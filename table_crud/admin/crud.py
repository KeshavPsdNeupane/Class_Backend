from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Admin
from .model import AdminCreate, AdminRead
from database import DB



async def create_new_admin(data:AdminCreate , db:DB):
    new_admin = Admin(**data.model_dump())
    db.add(new_admin)
    try:
        await db.commit()
        await db.refresh(new_admin)
        return new_admin
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Admin with user_id = {data.user_id} already exist"
            )
        elif "foreign key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"User with id = {data.user_id} not found"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )



async def get_admins(db:DB):
    result = await db.execute(select(Admin).order_by(Admin.user_id))
    return result.scalars().all()



async def delete_admin_by_id(user_id:int , db:DB):
    db_admin = await db.get(Admin , user_id)
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Admin with user id = {user_id} not found."
        )
    try:
        await db.delete(db_admin)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )