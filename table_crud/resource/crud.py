from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Resource
from .model import ResourceCreate
from database import DB


async def create_new_resource(data:ResourceCreate , db:DB):
    cleaned_data = {
        field: ( getattr(data ,field).strip() if isinstance(getattr(data, field),str) else getattr(data, field)) 
        for field in type(data).model_fields
    }
    new_resource = Resource(**cleaned_data)
    db.add(new_resource)
    try:
        await db.commit()
        await db.refresh(new_resource)
        return new_resource
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with user_id = {data.user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database Error"
        )


async def get_resources(db:DB):
    result = await db.execute(select(Resource).order_by(Resource.resource_id))
    return result.scalars().all()


async def get_resource_by_id(resource_id:int , db:DB):
    result = await db.get(Resource , resource_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with resource id = {resource_id} not found"
        )
    return result


async def delete_resource_by_id(resource_id:int , db:DB):
    db_resource = await db.get(Resource , resource_id)
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with resource id = {resource_id} not found"
        )
    try:
        await db.delete(db_resource)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot Resource User: related References exist"
        )
