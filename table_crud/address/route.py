from fastapi import APIRouter, status
from database import DB
from .model import AddressCreate, AddressRead, AddressUpdate
from .crud import (
    create_new_address,
    get_addresses,
    get_address_by_id,
    update_address_by_id,
    delete_address_by_id
)

address_route = APIRouter(prefix="/address", tags=["Address"])


@address_route.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(data: AddressCreate, db: DB):
    return await create_new_address(data, db)


@address_route.get("/", response_model=list[AddressRead])
async def read_addresses(db: DB):
    return await get_addresses(db)


@address_route.get("/{address_id}", response_model=AddressRead)
async def read_address(address_id: int, db: DB):
    return await get_address_by_id(address_id, db)


@address_route.put("/{address_id}", response_model=AddressRead)
async def update_address(address_id: int, data: AddressUpdate, db: DB):
    return await update_address_by_id(address_id, data, db)


@address_route.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, db: DB):
    await delete_address_by_id(address_id, db)
