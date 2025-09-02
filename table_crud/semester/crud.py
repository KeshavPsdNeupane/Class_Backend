from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Semester
from .model import SemesterCreate, SemesterUpdate
from database import DB

async def create_semester(data: SemesterCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_sem = Semester(**cleaned_data)
    db.add(new_sem)
    try:
        await db.commit()
        await db.refresh(new_sem)
        return new_sem
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if 'unique' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                  detail="Semester name must be unique"
            )
        elif 'foreign key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                  detail=f"Department with id = {data.department_id} not found."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
            )



async def get_all_semesters(db: DB):
    result = await db.execute(select(Semester).order_by(Semester.semester_id))
    return result.scalars().all()




async def get_semester_by_id(semester_id: int, db: DB):
    result = await db.get(Semester, semester_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Semester with id = {semester_id} not  found"
            )
    return result




async def update_semester(semester_id: int, data: SemesterUpdate, db: DB):
    db_sem = await db.get(Semester, semester_id)
    if not db_sem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Address with id = {semester_id} not found."
        )
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_sem, key, value)
    try:
        await db.commit()
        await db.refresh(db_sem)
        return db_sem
    except IntegrityError as e:
        await db.rollback()
        if 'unique' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
                , detail=f"Semester with this name {data.semester_name} already exists for the department."
            )
        elif 'foreign key' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                  detail=f"Invalid department_id {data.department_id} reference."
                )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
              detail="Database error"
            )



async def delete_semester_by_id(semester_id: int, db: DB):
    db_sem = await db.get(Semester, semester_id)
    if not db_sem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester with id = {semester_id} not found"
        )
    try:
        await db.delete(db_sem)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Semester : related References exist"
        )