from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import AdminAnnouncement
from .model import AdminAnnouncementCreate
from database import DB



async def create_new_admin_announcement(data:AdminAnnouncementCreate , db:DB):
    new_admin_announcement = AdminAnnouncement(**data.model_dump())
    db.add(new_admin_announcement)
    try:
        await db.commit()
        await db.refresh(new_admin_announcement)
        return new_admin_announcement
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "user_id" or "admin_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Admin with id = {data.admin_id} not found."
                ) 
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )



async def get_admin_announcements(db:DB):
    result = await db.execute(select(AdminAnnouncement).order_by(AdminAnnouncement.admin_announcement_id))
    return result.scalars().all()


async def get_admin_accouncement_by_id(admin_announcement_id:int , db:DB):
    result = await db.get(AdminAnnouncement, admin_announcement_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Admin Annoumcement with Id = {admin_announcement_id} not found"
        )
    return result


async def delete_admin_announcement_by_id(admin_announcement_id:int , db:DB):
    db_admin_announcement = await db.get(AdminAnnouncement,admin_announcement_id)
    if not db_admin_announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Admin Announcement with Id = {db_admin_announcement} not found"
        )
    try:
        await db.delete(db_admin_announcement)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )