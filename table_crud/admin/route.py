from fastapi import APIRouter , status
from database import DB
from .model import AdminCreate,AdminRead
from .crud import (
    get_admins,
    create_new_admin,
    delete_admin_by_id
)

admin_route = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@admin_route.post("/", response_model= AdminCreate)
async def create_admin(data:AdminCreate , db:DB):
    return await create_new_admin(data , db)


@admin_route.get("/", response_model= list[AdminRead])
async def read_admin(db:DB):
    return await get_admins(db)

@admin_route.delete("/{user_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_admin(user_id:int , db:DB):
    await delete_admin_by_id(user_id , db)
    