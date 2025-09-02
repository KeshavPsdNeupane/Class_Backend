from fastapi import APIRouter, status
from database import DB
from .model import DepartmentCreate, DepartmentRead, DepartmentUpdate
from .crud import (
    create_new_department,
    get_departments,
    get_department_by_id,
    update_department_by_id,
    delete_department_by_id
)

department_route = APIRouter(prefix="/department", tags=["Department"])

@department_route.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(data: DepartmentCreate, db: DB):
    return await create_new_department(data, db)

@department_route.get("/", response_model=list[DepartmentRead])
async def read_departments(db: DB):
    return await get_departments(db)

@department_route.get("/{dept_id}", response_model=DepartmentRead)
async def read_department_by_id(dept_id: int, db: DB):
    return await get_department_by_id(dept_id, db)

@department_route.put("/{dept_id}", response_model=DepartmentRead)
async def update_department(dept_id: int, data: DepartmentUpdate, db: DB):
    return await update_department_by_id(dept_id, data, db)

@department_route.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(dept_id: int, db: DB):
    await delete_department_by_id(dept_id, db)
