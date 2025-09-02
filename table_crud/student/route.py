from fastapi import APIRouter , status
from database import DB
from .model import StudentCreate,StudentRead
from .crud import (
    get_students,
    create_new_student,
    delete_student_by_id
)

student_route = APIRouter(
    prefix="/student",
    tags=["Student"]
)


@student_route.post("/", response_model= StudentCreate)
async def create_student(data:StudentCreate , db:DB):
    return await create_new_student(data , db)


@student_route.get("/", response_model= list[StudentRead])
async def read_student(db:DB):
    return await get_students(db)

@student_route.delete("/{user_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_student(user_id:int , db:DB):
    await delete_student_by_id(user_id , db)