from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from dmodels import Role
from .model import RoleCreate, RoleUpdate


async def create_new_role(data: RoleCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_role = Role(**cleaned_data)
    db.add(new_role)
    try:
        await db.commit()
        await db.refresh(new_role)
        return new_role
    except IntegrityError as e:
        await db.rollback()
        if 'unique' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role with name '{data.role_name}' already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error"
        )


async def get_roles(db: DB):
    result = await db.execute(select(Role).order_by(Role.role_name))
    return result.scalars().all()


async def get_role_by_name(role_name: str, db: DB):
    role = await db.get(Role, role_name)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with name '{role_name}' not found"
        )
    return role


async def update_role_by_name(role_name: str, data: RoleUpdate, db: DB):
    db_role = await db.get(Role, role_name)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with name '{role_name}' not found"
        )
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_role, key, value)
    try:
        await db.commit()
        await db.refresh(db_role)
        return db_role
    except IntegrityError as e:
        await db.rollback()
        if 'unique' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role with name '{data.role_name}' already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error"
        )


async def delete_role_by_name(role_name: str, db: DB):
    db_role = await db.get(Role, role_name)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with name '{role_name}' not found"
        )
    try:
        await db.delete(db_role)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Role: related references exist"
        )
