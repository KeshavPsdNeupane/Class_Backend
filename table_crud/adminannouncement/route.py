from fastapi import APIRouter , status
from database import DB
from .model import AdminAnnouncementCreate,AdminAnnouncementRead
from .crud import(
    get_admin_announcements,
    get_admin_accouncement_by_id,
    create_new_admin_announcement,
    delete_admin_announcement_by_id,
)

admin_announcement_route = APIRouter(
    prefix= "/adminannouncement",
    tags = ["Admin Announcement"]
)



@admin_announcement_route.post("/" , response_model= AdminAnnouncementCreate)
async def create_admin_announcement(data:AdminAnnouncementCreate,db:DB):
    return await create_new_admin_announcement(data , db)



@admin_announcement_route.get("/", response_model=list[AdminAnnouncementRead] )
async def read_admin_annoucements(db:DB):
    return await get_admin_announcements(db)

@admin_announcement_route.get("/{admin_announcement_id}" , response_model= AdminAnnouncementRead)
async def read_admin_annoucement(admin_announcement_id:int ,db:DB):
    return await get_admin_accouncement_by_id(admin_announcement_id ,db)


@admin_announcement_route.delete("/{admin_announcement_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_admin_announcement(admin_announcement_id:int , db:DB):
    await delete_admin_announcement_by_id(admin_announcement_id , db)
