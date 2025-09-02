from fastapi import APIRouter , status
from .model import ResourceCreate,ResourceRead
from database import DB
from .crud import (
    get_resources,
    get_resource_by_id,
    create_new_resource,
    delete_resource_by_id,
)
resource_route = APIRouter(
    prefix="/resource",
    tags=["Resource"]
)


@resource_route.post("/" , response_model= ResourceCreate)
async def create_resource(data:ResourceCreate, db:DB):
    return await create_new_resource(data , db)


@resource_route.get("/" , response_model= list[ResourceRead])
async def read_resources(db:DB):
    return await get_resources(db)

@resource_route.get("/{resource_id}", response_model = ResourceRead)
async def read_resource(resource_id:int,db:DB):
    return await get_resource_by_id(resource_id, db)

@resource_route.delete("/{resouce_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_resouce(resource_id:int , db:DB):
    await delete_resource_by_id(resource_id , db)