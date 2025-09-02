from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from dmodels import Address
from .model import AddressCreate, AddressUpdate
from database import DB


async def create_new_address(data: AddressCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_address = Address(**cleaned_data)
    db.add(new_address)
    try:
        await db.commit()
        await db.refresh(new_address)
        return new_address
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if 'unique' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                  detail="Address with the given detail already exist"
                )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
              detail="Database Error"
            )



async def get_addresses(db: DB):
    result = await db.execute(select(Address).order_by(Address.address_id))
    return result.scalars().all()


async def get_address_by_id(address_id: int, db: DB):
    address = await db.get(Address, address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id = {address_id} not found."
        )
    return address


async def update_address_by_id(address_id: int, data: AddressUpdate, db: DB):
    db_address = await db.get(Address, address_id)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id = {address_id} not found."
        )

    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_address, key, value)

    try:
        await db.commit()
        await db.refresh(db_address)
        return db_address
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "unique" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Address with the given detail already exist"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database error."
            )





async def delete_address_by_id(address_id: int, db: DB):
    db_address = await db.get(Address, address_id)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id = {address_id} not found."
        )
    try:
        await db.delete(db_address)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Address: related References exist."
        )