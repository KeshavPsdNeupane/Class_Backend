from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Student
from .model import StudentCreate
from database import DB



async def create_new_student(data:StudentCreate , db:DB):
    new_student = Student(**data.model_dump())
    db.add(new_student)
    try:
        await db.commit()
        await db.refresh(new_student)
        return new_student
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Student with user_id = {data.user_id} already exist"
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



async def get_students(db:DB):
    result = await db.execute(select(Student).order_by(Student.user_id))
    return result.scalars().all()



async def delete_student_by_id(user_id:int , db:DB):
    db_student = await db.get(Student , user_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Student with user id = {user_id} not found."
        )
    try:
        await db.delete(db_student)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )