from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import User
from .model import UserCreate, UserUpdate
from database import DB


async def create_new_user(data:UserCreate , db:DB):
    cleaned_data = {
        field:(getattr(data , field).strip() if isinstance(getattr(data , field) , str) else getattr(data , field))
        for field in type(data).model_fields
    }
    new_user = User(**cleaned_data)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "role" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"role with id = {data.role_id} not found."
                )  
            elif "user_detail" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"user_detail with id = {data.user_detail_id} not found."
                )  
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
        )    
        elif "unique" in error_msg:
           if "user_detail" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Userdetail must be unique"
                ) 
           elif "email" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Email must be unique"
                ) 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )
        

async def get_users(db:DB):
    result = await db.execute(select(User).order_by(User.user_id))
    return result.scalars().all()


async def get_user_by_id(user_id:int , db:DB):
    result = await db.get(User , user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"user with userid = {user_id} not found"
        )
    return result


async def update_user_by_id(user_id:int, data:UserUpdate , db:DB):
    db_user = await db.get(User ,user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Address with id = {user_id} not found."
        )
    updates = {
        key: (value.strip()if isinstance(value , str)else value)
        for key,value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_user,key,value)
    
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "role" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"role with id = {data.role_id} not found."
                )  
            elif "user_detail" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"user_detail with id = {data.user_detail_id} not found."
                )  
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
        )    
        elif "unique" in error_msg:
           if "user_detail" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Userdetail must be unique"
                ) 
           elif "email" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Email must be unique"
                ) 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )




async def delete_user_by_id(user_id: int, db: DB):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id = {user_id} not found"
        )
    try:
        await db.delete(db_user)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete User: related References exist"
        )
