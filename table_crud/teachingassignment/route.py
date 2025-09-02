from fastapi import APIRouter , status
from database import DB
from .model import(
    TeachAssignCreate,
    TeachAssignDelete,
    TeachAssignRead,
)
from .crud import (
    get_teach_assigns,
    create_new_teach_assign,
    delete_teach_assign_by_ides
)

teach_assign_route = APIRouter(
    prefix="/teachassign",
    tags=["Teaching Assignment"]
)

@teach_assign_route.get("/", response_model= list[TeachAssignRead])
async def read_teach_assign(db:DB):
    return await get_teach_assigns(db)

@teach_assign_route.post("/" , response_model= TeachAssignCreate)
async def create_teach_assign(data:TeachAssignCreate , db:DB):
    return await create_new_teach_assign(data , db)

@teach_assign_route.delete("/" , response_model= TeachAssignDelete)
async def delete_tech_assign_by_id(ids:TeachAssignDelete , db:DB):
    await delete_teach_assign_by_ides(ids , db)
