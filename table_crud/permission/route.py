from fastapi import APIRouter, status
from database import DB
from .model import PermissionCreate, PermissionRead, PermissionUpdate
from .crud import (
    get_permissions,
    get_permission_by_name,
    create_new_permission,
    update_permission_by_name,
    delete_permission_by_name
)

permission_route = APIRouter(prefix="/permissions", tags=["Permission"])


@permission_route.post("/", response_model=PermissionCreate)
async def create_permission(permission_data: PermissionCreate, db: DB):
    return await create_new_permission(permission_data, db)


@permission_route.get("/", response_model=list[PermissionRead])
async def read_permissions(db: DB):
    return await get_permissions(db)


@permission_route.get("/{permission_name}", response_model=PermissionRead)
async def read_permission(permission_name: str, db: DB):
    return await get_permission_by_name(permission_name, db)


@permission_route.put("/{permission_name}", response_model=PermissionUpdate)
async def update_permission(permission_name: str, new_permission_data: PermissionUpdate, db: DB):
    return await update_permission_by_name(permission_name, new_permission_data, db)


@permission_route.delete("/{permission_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(permission_name: str, db: DB):
    await delete_permission_by_name(permission_name, db)
