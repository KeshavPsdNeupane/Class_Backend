from fastapi import APIRouter , status
from database import DB
from .model import TeacherCreate,TeacherRead
from .crud import (
    get_teachers,
    create_new_teacher,
    delete_teacher_by_id
)

teacher_route = APIRouter(
    prefix="/teacher",
    tags=["Teacher"]
)


@teacher_route.post("/", response_model= TeacherCreate)
async def create_admin(data:TeacherCreate , db:DB):
    return await create_new_teacher(data , db)


@teacher_route.get("/", response_model= list[TeacherRead])
async def read_admin(db:DB):
    return await get_teachers(db)

@teacher_route.delete("/{user_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_admin(user_id:int , db:DB):
    await delete_teacher_by_id(user_id , db)