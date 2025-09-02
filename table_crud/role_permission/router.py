from fastapi import APIRouter , status
from database import DB
from .model import (
    RolePermissionCreateDelete,
    RolePermissionRead ,
    RolePermissionReadByPermission,
    RolePermissionReadByRole
)
from .crud import (
    create_new_role_permission,
    get_role_permissions,
    get_role_permission_by_role,
    get_role_permission_by_permission,
    delete_role_permission
)




role_permission_route = APIRouter(
    prefix="/roleperm",
    tags=["Role Permission"]
)


@role_permission_route.post("/" , response_model= RolePermissionCreateDelete)
async def create_role_permisson(role_permission_data:RolePermissionCreateDelete , db:DB):
    return await create_new_role_permission(role_permission_data,db)



@role_permission_route.get("/" ,  response_model= list[RolePermissionRead])
async def read_role_perms(db:DB):
    return await get_role_permissions(db)



@role_permission_route.get("/permission/{role_id}", response_model= list[RolePermissionReadByRole])
async def read_role_perm_by_role(role_id:str , db:DB):
    return await get_role_permission_by_role(role_id , db)


@role_permission_route.get("/role/{perm_id}", response_model= list[RolePermissionReadByPermission])
async def read_role_perm_by_permission(perm_id:str , db:DB):
    return await get_role_permission_by_permission(perm_id , db)


@role_permission_route.delete("/" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_role_perm(data:RolePermissionCreateDelete , db:DB):
    return await delete_role_permission(data , db)
