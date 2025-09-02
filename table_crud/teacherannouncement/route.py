from fastapi import APIRouter , status
from database import DB
from .model import TeacherAnnouncementCreate,TeacherAnnouncementRead
from .crud import(
    get_teach_annuncements,
    create_new_teach_announcement,
    delete_teach_announcement_by_id,
    get_teach_announcment_by_id
)


teach_announcement_route = APIRouter(
    prefix="/teachannouncement",
    tags=["Teacher Announcement"]
)

@teach_announcement_route.post("/", response_model= TeacherAnnouncementCreate)
async def create_teach_annoouncement(data:TeacherAnnouncementCreate, db:DB):
    return await create_new_teach_announcement(data, db)



@teach_announcement_route.get("/", response_model= list[TeacherAnnouncementRead])
async def read_teach_announcements(db:DB):
    return await get_teach_annuncements(db)


@teach_announcement_route.get("/{teach_announcement_id}" , response_model= TeacherAnnouncementRead)
async def read_teach_announcement(teach_announcement_id:int ,  db:DB):
    return await get_teach_announcment_by_id(teach_announcement_id, db)


@teach_announcement_route.delete("/{teach_announcement_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_teach_announcement(teach_announcement_id:int , db:DB):
    await delete_teach_announcement_by_id(teach_announcement_id , db)