from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Subject
from .model import SubjectCreate, SubjectUpdate
from database import DB


async def create_new_subject(data:SubjectCreate ,  db:DB):
    cleaned_data = {
        field: (getattr(data , field).strip() if isinstance(getattr(data , field),str)else getattr(data , field))
        for field in type(data).model_fields
    }
    new_subject = Subject(**cleaned_data)
    db.add(new_subject)
    try:
        await db.commit()
        await db.refresh(new_subject)
        return new_subject
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            if "subject_name" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subject name = {data.subject_name} already exits. "
            )
            elif "subject_code" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"subject code = {data.subject_code} already exits. "
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Unique constraints error"
            )
        elif 'foreign key' in error_msg:
            if "semester_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Semester with id = {data.semester_id} not found"
            )
            elif "resource_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"resource with id = {data.resource_id} not found"
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Foreign Key Reference Constraint Error"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )



async def get_subjects(db:DB):
    result = await db.execute(select(Subject).order_by(Subject.subject_id))
    return result.scalars().all()



async def get_subject_by_id(subject_id:int , db:DB):
    result = await db.get(Subject, subject_id)
    if not result:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Subject with subject_id = {subject_id} not found"
        )
    return result




async def update_subject_by_id(subject_id:int , data:SubjectUpdate , db:DB):
    db_subject = await db.get(Subject , subject_id)
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Address with id = {subject_id} not found."
        )
    updates = {
        key: (value.strip() if isinstance(value , str) else value)
        for key , value in data.model_dump(exclude_unset=True).items()
    }
    for key,value in updates.items():
        setattr(db_subject , key, value)
    try:
        await db.commit()
        await db.refresh(db_subject)
        return db_subject
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            if "subject_name" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subject name = {data.subject_name} already exits. "
            )
            elif "subject_code" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"subject code = {data.subject_code} already exits. "
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Unique constraints error"
            )
        elif 'foreign key' in error_msg:
            if "semester_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Semester with id = {data.semester_id} not found"
            )
            elif "resource_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"resource with id = {data.resource_id} not found"
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Foreign Key Reference Constraint Error"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
            )



async def delete_subject_by_id(subject_id:int , db:DB):
    db_subject = await db.get(Subject , subject_id)
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Address with id = {db_subject} not found."
        )
    try:
        await db.delete(db_subject)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Subject : related References exist"
        )