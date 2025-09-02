# routes.py
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from .model import UserDetailCreate, UserDetailUpdate
from dmodels import UserDetails


async def create_new_user_detail(data: UserDetailCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_detail = UserDetails(**cleaned_data)
    db.add(new_detail)
    try:
        await db.commit()
        await db.refresh(new_detail)
        return new_detail
    except IntegrityError as e:
        await db.rollback()
        error_msg: str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "address" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Address with id = {data.address_id} not found."
                )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Referential integrity invalid"
            )
        if "gender" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Gender must be male or female"
            )
        if "age" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid age value"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database Error"
        )


async def get_user_details(db: DB):
    result = await db.execute(select(UserDetails).order_by(UserDetails.user_detail_id))
    return result.scalars().all()


async def get_user_detail_by_id(user_detail_id: int, db: DB):
    result = await db.get(UserDetails, user_detail_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User detail with id = {user_detail_id} was not found"
        )
    return result


async def update_user_detail_by_id(user_detail_id: int, data: UserDetailUpdate, db: DB):
    db_user_detail = await db.get(UserDetails, user_detail_id)
    if not db_user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user_detail with id = {user_detail_id} was not found"
        )
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_user_detail, key, value)
    try:
        await db.commit()
        await db.refresh(db_user_detail)
        return db_user_detail
    except IntegrityError as e:
        await db.rollback()
        error_msg: str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "address" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Address with id = {data.address_id} not found."
                )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Referential integrity invalid"
            )
        if "gender" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Gender must be male, female or other"
            )
        if "age" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid age value"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database Error"
        )


async def delete_user_detail_by_id(user_detail_id: int, db: DB):
    db_user_detail = await db.get(UserDetails, user_detail_id)
    if not db_user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user_detail with id = {user_detail_id} was not found"
        )
    try:
        await db.delete(db_user_detail)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete UserDetail : related References exist"
        )
