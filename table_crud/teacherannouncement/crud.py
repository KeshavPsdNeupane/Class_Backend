from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import TeacherAnnouncement
from .model import TeacherAnnouncementCreate
from database import DB


async def create_new_teach_announcement(data:TeacherAnnouncementCreate , db:DB):
    new_teach_announcement = TeacherAnnouncement(**data.model_dump())
    db.add(new_teach_announcement)
    try:
        await db.commit()
        await db.refresh(new_teach_announcement)
        return new_teach_announcement
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "user_id" or "admin_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Teacher with id = {data.teacher_id} not found."
                ) 
            elif "department_id"  in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Department with id = {data.department_id} not found."
                ) 
            elif "section_id"  in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Section with id = {data.section_id} not found."
                )
            elif "subject_id"  in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Subject with id = {data.subject_id} not found."
                )
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )



async def get_teach_annuncements(db:DB):
    result = await db.execute(select(TeacherAnnouncement).order_by(TeacherAnnouncement.teacher_announcement_id))
    return result.scalars().all()


async def get_teach_announcment_by_id(teach_announcement_id:int , db:DB):
    result = await db.get(TeacherAnnouncement, teach_announcement_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Teach Annoumcement with Id = {teach_announcement_id} not found"
        )
    return result


async def delete_teach_announcement_by_id(teach_announcement_id:int , db:DB):
    db_teach_announcement = await db.get(TeacherAnnouncement,teach_announcement_id)
    if not db_teach_announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Teacher Announcement with Id = {db_teach_announcement} not found"
        )
    try:
        await db.delete(db_teach_announcement)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )