from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Teacher
from .model import TeacherCreate
from database import DB



async def create_new_teacher(data:TeacherCreate , db:DB):
    new_teacher = Teacher(**data.model_dump())
    db.add(new_teacher)
    try:
        await db.commit()
        await db.refresh(new_teacher)
        return new_teacher
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Teacher with user_id = {data.user_id} already exist"
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



async def get_teachers(db:DB):
    result = await db.execute(select(Teacher).order_by(Teacher.user_id))
    return result.scalars().all()



async def delete_teacher_by_id(user_id:int , db:DB):
    db_teacher = await db.get(Teacher , user_id)
    if not db_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Teacher with user id = {user_id} not found."
        )
    try:
        await db.delete(db_teacher)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )