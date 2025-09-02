from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException ,status
from database import DB
from .model import  TeachAssignCreate,TeachAssignDelete
from dmodels import TeachingAssignment


async def create_new_teach_assign(data:TeachAssignCreate ,db:DB):
    cleaned_data = {
        field: (getattr(data,field).strip() if isinstance(getattr(data,field) , str) else getattr(data,field))
        for field in type(data).model_fields
    }
    new_teach_assign  = TeachingAssignment(**cleaned_data)
    db.add(new_teach_assign)
    try:
        await db.commit()
        await db.refresh(new_teach_assign)
        return new_teach_assign
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "teacher_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Teacher with id = {data.teacher_id} not found."
                )  
            elif "subject_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Subject with id = {data.subject_id} not found."
                )
            elif "section_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Section with id = {data.section_id} not found."
                )  
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )



async def get_teach_assigns(db:DB):
    result = await db.execute(select(TeachingAssignment).order_by(TeachingAssignment.teacher_id))
    return result.scalars().all()



async def delete_teach_assign_by_ides(ids: TeachAssignDelete, db: DB):
    stml = (
        select(TeachingAssignment).where(
            (TeachingAssignment.teacher_id == ids.teacher_id) &
            (TeachingAssignment.section_id == ids.section_id) &
            (TeachingAssignment.subject_id == ids.subject_id)
        )
    )
    result = await db.execute(stml)
    db_teach_assign = result.scalar_one_or_none()
    if not db_teach_assign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher with given detail was not found"
        )
    try:
        await db.delete(db_teach_assign)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database Error"
        )

