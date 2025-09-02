from sqlalchemy.future import select 
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from .model import RolePermissionCreateDelete, RolePermissionRead
from dmodels import role_permission, Permission, Role
from sqlalchemy import insert, delete


async def create_new_role_permission(role_permission_data: RolePermissionCreateDelete, db: DB):
    stmt = insert(role_permission).values(
        role_name=role_permission_data.role_name,
        permission_name=role_permission_data.permission_name
    )
    try:
        await db.execute(stmt)
        await db.commit()
        return role_permission_data
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig).lower()
        if "foreign key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role_name or permission_name: related record does not exist."
            )
        elif "unique" in error_msg or "duplicate" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"RolePermission with role_name={role_permission_data.role_name} "
                    f"and permission_name={role_permission_data.permission_name} already exists."
                )
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Error."
            )


async def get_role_permissions(db: DB):
    result = await db.execute(
        select(role_permission).order_by(role_permission.c.role_name, role_permission.c.permission_name)
    )
    return result.mappings().all()


async def get_role_permission_by_role(role_name: str, db: DB):
    stmt = (
        select(Permission)
        .join(role_permission, Permission.permission_name == role_permission.c.permission_name)
        .where(role_permission.c.role_name == role_name)
    )
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    if not permissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RolePermission with role_name = {role_name} not found"
        )
    return permissions


async def get_role_permission_by_permission(permission_name: str, db: DB):
    stmt = (
        select(Role)
        .join(role_permission, Role.role_name == role_permission.c.role_name)
        .where(role_permission.c.permission_name == permission_name)
    )
    result = await db.execute(stmt)
    roles = result.scalars().all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RolePermission with permission_name = {permission_name} not found"
        )
    return roles


async def delete_role_permission(data: RolePermissionCreateDelete, db: DB):
    stmt = (
        delete(role_permission)
        .where(
            (role_permission.c.role_name == data.role_name) &
            (role_permission.c.permission_name == data.permission_name)
        )
        .returning(role_permission.c.role_name)
    )
    result = await db.execute(stmt)
    deleted = result.fetchone()
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role-permission pair not found"
        )
    await db.commit()
