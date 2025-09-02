from fastapi import APIRouter , status
from database import DB
from .model import SubjectCreate,SubjectRead,SubjectUpdate
from .crud import(
    get_subjects,
    get_subject_by_id,
    create_new_subject,
    update_subject_by_id,
    delete_subject_by_id
)


subject_route = APIRouter(
    prefix="/subject",
    tags=["Subject"]
)


@subject_route.post("/", response_model= SubjectCreate)
async def create_subject(data:SubjectCreate , db:DB):
    return await create_new_subject(data , db)



@subject_route.get("/", response_model= list[SubjectRead])
async def read_subjects(db:DB):
    return await get_subjects(db)


@subject_route.get("/{subject_id}", response_model= list[SubjectRead])
async def read_subject(subject_id:int ,db:DB):
    return await get_subject_by_id(subject_id,db)


@subject_route.put("/{subject_id}" ,  response_model= SubjectUpdate)
async def update_subject(subject_id:int , data:SubjectUpdate , db:DB):
    return await update_subject_by_id(subject_id , data , db)

@subject_route.delete("/{subject_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id:int , db:DB):
    await delete_subject_by_id(subject_id , db)
    