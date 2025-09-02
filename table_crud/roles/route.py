from fastapi import APIRouter, status
from database import DB
from .model import RoleCreate, RoleRead, RoleUpdate
from .crud import (
    get_roles,
    get_role_by_name,
    create_new_role,
    update_role_by_name,
    delete_role_by_name
)

role_route = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@role_route.post("/", response_model=RoleCreate)
async def create_role(role_data: RoleCreate, db: DB):
    return await create_new_role(role_data, db)


@role_route.get("/", response_model=list[RoleRead])
async def read_roles(db: DB):
    return await get_roles(db)


@role_route.get("/{role_name}", response_model=RoleRead)
async def read_role(role_name: str, db: DB):
    return await get_role_by_name(role_name, db)


@role_route.put("/{role_name}", response_model=RoleUpdate)
async def update_role(role_name: str, new_role_data: RoleUpdate, db: DB):
    return await update_role_by_name(role_name, new_role_data, db)


@role_route.delete("/{role_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_name: str, db: DB):
    await delete_role_by_name(role_name, db)
