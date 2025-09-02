from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from pydantic import EmailStr
from dmodels import Address, UserDetails, User, Role, Admin, Student, Teacher
from .model import UserDetailData, AddressData, UserCreateData, UserRestDetail, StudentOnlyDetail
from table_crud.userdetail.model import UserDetailCreate
from table_crud.user.model import UserCreate
from auth.cryptography import get_hashed_password, create_password
from project_email import send_email_async
from table_crud.admin.model import AdminCreate
from table_crud.teacher.model import TeacherCreate
from table_crud.student.model import StudentCreate
from custom_http_error import CustomHttpError,HttpErrorMessages


async def user_register(data: UserCreateData, db: DB):
    await does_email_exists(data.user_rest_detail.email_id, db)

    async with db.begin_nested():
        user_address_id = await get_or_create_address_id(data.address_data, db)
        user_detail_id = await get_user_detail_id_and_create_user_detail_in_db(
            data.user_detail_data, user_address_id, db
        )

    user_rest_data: UserRestDetail = data.user_rest_detail
    email_id: str = user_rest_data.email_id
    password: str = create_password(10)
    role_name: str = await check_role_name(user_rest_data.role_name, db)

    user = UserCreate(
        email_id=email_id,
        user_detail_id=user_detail_id,
        hashed_pw=get_hashed_password(password),
        role_name=role_name
    )
    new_user: User = User(**user.model_dump())
    db.add(new_user)

    try:
        await db.flush()
        await add_to_respective_role_table(data, new_user, db)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError as e:
        await db.rollback()
        error_msg: str = str(e.orig).lower()
        if "foreign key" in error_msg:
            raise CustomHttpError.UnprocessableEntity_422(HttpErrorMessages.REFERENTIAL_INTEGRITY_UNPROCESSABLE_422())
        raise CustomHttpError.InternalServerError_500(error_msg)
    except Exception as e:
        await db.rollback()
        raise CustomHttpError.InternalServerError_500(str(e))
    await send_email_async(email_id, "Account Creation", password)


async def get_or_create_address_id(data: AddressData, db: DB):
    result = await db.execute(
        select(Address.address_id).where(
            (Address.province_name == data.province_name) &
            (Address.district_name == data.district_name) &
            (Address.village_city_name == data.village_city_name) &
            (Address.ward_number == data.ward_number) &
            (Address.place_name == data.place_name)
        )
    )
    db_address_id = result.scalar_one_or_none()
    if db_address_id:
        return db_address_id

    new_address = Address(**data.model_dump())
    db.add(new_address)
    await db.flush()
    return new_address.address_id


async def get_user_detail_id_and_create_user_detail_in_db(data: UserDetailData, user_address_id: int, db: DB):
    user_detail_data = UserDetailCreate(
        **data.model_dump(exclude={"gender"}),
        gender=data.gender.lower(),
        address_id=user_address_id
    )
    new_user_detail = UserDetails(**user_detail_data.model_dump())
    db.add(new_user_detail)
    await db.flush()
    return new_user_detail.user_detail_id


async def check_role_name(role_name: str, db: DB) -> str:
    result = await db.execute(
        select(Role.role_name).where(Role.role_name == role_name.lower())
    )
    db_role_name = result.scalar_one_or_none()
    if db_role_name is None:
        raise CustomHttpError.NotFound_404(HttpErrorMessages.SOMETHING_NOTFOUND_404("Role" , role_name))
    return db_role_name


async def does_email_exists(email: EmailStr, db: DB) -> None:
    try:
        result = await db.execute(select(User.user_id).where(User.email_id == email))
        existing = result.scalar_one_or_none()
        if existing is not None:
            raise CustomHttpError.Conflict_409(HttpErrorMessages.EMAIL_CONFLICT_409)
    except Exception as e:
        raise CustomHttpError.InternalServerError_500(f"Error while checking Email {str(e)}")


async def add_to_respective_role_table(data: UserCreateData, user: User, db: DB):
    user_role = user.role_name.lower()
    user_id = user.user_id

    if user_role == "admin":
        new_admin_data = AdminCreate(user_id=user_id)
        new_admin = Admin(**new_admin_data.model_dump())
        db.add(new_admin)

    elif user_role == "teacher":
        new_teacher_data = TeacherCreate(user_id=user_id)
        new_teacher = Teacher(**new_teacher_data.model_dump())
        db.add(new_teacher)

    elif user_role == "student":
        student_only = data.studentOnly
        if student_only is None:
            raise CustomHttpError.BadRequest_400(
                HttpErrorMessages.INPUTFIELD_EMPTY_BADREQUEST_400("Student-specific data"))
        if student_only.batch_no is None:
            raise CustomHttpError.BadRequest_400(
                HttpErrorMessages.INPUTFIELD_EMPTY_BADREQUEST_400("Batch number","for student"))
        if student_only.section_id is None:
            raise  CustomHttpError.BadRequest_400(
                HttpErrorMessages.INPUTFIELD_EMPTY_BADREQUEST_400("Section ID","for student"))
        new_student_data = StudentCreate(
            user_id=user_id,
            batch_name=student_only.batch_no,
            section_id=student_only.section_id
        )
        new_student = Student(**new_student_data.model_dump())
        db.add(new_student)
