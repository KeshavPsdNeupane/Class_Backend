from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from .model import PermissionCreate, PermissionUpdate
from dmodels import Permission


async def create_new_permission(data: PermissionCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_permission = Permission(**cleaned_data)
    db.add(new_permission)
    try:
        await db.commit()
        await db.refresh(new_permission)
        return new_permission
    except IntegrityError as e:
        await db.rollback()
        if 'unique' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Permission with name '{data.permission_name}' already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error"
        )


async def get_permissions(db: DB):
    result = await db.execute(select(Permission).order_by(Permission.permission_name))
    return result.scalars().all()


async def get_permission_by_name(permission_name: str, db: DB):
    permission = await db.get(Permission, permission_name)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with name '{permission_name}' not found"
        )
    return permission


async def update_permission_by_name(permission_name: str, data: PermissionUpdate, db: DB):
    db_permission = await db.get(Permission, permission_name)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with name '{permission_name}' not found"
        )
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_permission, key, value)
    try:
        await db.commit()
        await db.refresh(db_permission)
        return db_permission
    except IntegrityError as e:
        await db.rollback()
        if 'unique' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Permission with name '{data.permission_name}' already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error"
        )


async def delete_permission_by_name(permission_name: str, db: DB):
    db_permission = await db.get(Permission, permission_name)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with name '{permission_name}' not found"
        )
    await db.delete(db_permission)
    await db.commit()
