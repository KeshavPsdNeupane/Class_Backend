from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from    custom_http_error import CustomHttpError,HttpErrorMessages
from dmodels import User
from .model import PasswordChange
from database import DB
from auth.cryptography import verify_password, get_hashed_password


async def password_change(user: User, data: PasswordChange, db: DB):
    db_user = await get_db_user_by_id(user.user_id, db)
    check_if_old_pw_and_new_are_same(data)
    check_if_pw_and_confirm_are_same(data)
    if not verify_password(data.old_password, db_user.hashed_pw):
        raise CustomHttpError.NotFound_404("Incorrect Password")
    db_user.hashed_pw = get_hashed_password(data.new_password)
    try:
        await db.commit()
        await db.refresh(db_user)
    except InvalidRequestError:
        await db.rollback()
        raise CustomHttpError.Conflict_409(HttpErrorMessages.SESSION_BUSY_CONFLICT_409)
    except IntegrityError:
        await db.rollback()
        raise  CustomHttpError.UnprocessableEntity_422(HttpErrorMessages.REFERENTIAL_INTEGRITY_UNPROCESSABLE_422())
    except Exception as e:
        await db.rollback()
        raise CustomHttpError.InternalServerError_500("Couldnt Change the password.")


def check_if_pw_and_confirm_are_same(data: PasswordChange):
    if data.confirm_password != data.new_password:
        raise CustomHttpError.BadRequest_400("Password and confirm password do not match")


def check_if_old_pw_and_new_are_same(data: PasswordChange):
    if data.old_password == data.new_password:
        raise CustomHttpError.BadRequest_400("Old and new password cannot be the same")

async def get_db_user_by_id(user_id: int, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise CustomHttpError.InternalServerError_500()
    return user
