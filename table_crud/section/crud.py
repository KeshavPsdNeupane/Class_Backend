# crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from dmodels import Section  
from .model import SectionCreate, SectionUpdate 


async def create_section(data: SectionCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_section = Section(**cleaned_data)
    db.add(new_section)
    try:
        await db.commit()
        await db.refresh(new_section)
        return new_section
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Section with given detail already exist."
            )
        elif "foreign key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Semester with id = {data.semester_id} not found."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database Error"
        )


async def get_sections(db: DB):
    result = await db.execute(select(Section).order_by(Section.section_id))
    return result.scalars().all()



async def get_section_by_id(section_id: int, db: DB):
    result = await db.get(Section, section_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id = {section_id} not found."
        )
    return result



async def update_section_by_id(section_id: int, data: SectionUpdate, db: DB):
    db_section = await db.get(Section, section_id)
    if not db_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id = {section_id} not found."
        )
    
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_section, key, value)
    
    try:
        await db.commit()
        await db.refresh(db_section)
        return db_section
    except IntegrityError as e:
        await db.rollback()
        if "unique" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Section with this name {data.section_name} already exists for the semester."
            )
        elif "foreign key" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Invalid semester_id {data.semester_id} reference."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database error."
            )



async def delete_section_by_id(section_id: int, db: DB):
    db_section = await db.get(Section, section_id)
    if not db_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id = {section_id} not found."
        )
    try:
        await db.delete(db_section)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Section : related References exist"
        )
