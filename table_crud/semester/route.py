from fastapi import APIRouter, status
from database import DB
from .model import SemesterCreate, SemesterRead, SemesterUpdate
from .crud import (
    create_semester,
    get_all_semesters,
    get_semester_by_id,
    update_semester,
    delete_semester_by_id
)

semester_route = APIRouter(prefix="/semester", tags=["Semester"])

@semester_route.post("/", response_model=SemesterRead, status_code=status.HTTP_201_CREATED)
async def create(data: SemesterCreate, db: DB):
    return await create_semester(data, db)

@semester_route.get("/", response_model=list[SemesterRead])
async def read_all(db: DB):
    return await get_all_semesters(db)

@semester_route.get("/{semester_id}", response_model=SemesterRead)
async def read_one(semester_id: int, db: DB):
    return await get_semester_by_id(semester_id, db)

@semester_route.put("/{semester_id}", response_model=SemesterRead)
async def update(semester_id: int, data: SemesterUpdate, db: DB):
    return await update_semester(semester_id, data, db)

@semester_route.delete("/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(semester_id: int, db: DB):
    await delete_semester_by_id(semester_id, db)
