from fastapi import APIRouter , status
from database import DB
from .model import UserDetailCreate,UserDetailRead,UserDetailUpdate
from .crud import (
    create_new_user_detail,
    get_user_details,
    get_user_detail_by_id,
    update_user_detail_by_id,
    delete_user_detail_by_id
)

user_detail_route  = APIRouter(prefix="/userdetail",tags=["User Detail"])


@user_detail_route.post("/", response_model= UserDetailCreate)
async def create_user_detail(data:UserDetailCreate, db:DB):
    return await create_new_user_detail(data , db)


@user_detail_route.get("/" ,  response_model= list[UserDetailRead])
async def read_user_details(db:DB):
    return await get_user_details(db)

@user_detail_route.get("/{user_detail_id}" , response_model=UserDetailRead)
async def read_user_detail(user_detail_id:int ,db:DB):
    return await get_user_detail_by_id(user_detail_id , db)

@user_detail_route.put("/{user_detail_id}" , response_model=UserDetailUpdate)
async def update_user_detail(user_detail_id:int , data:UserDetailUpdate , db:DB):
    return await update_user_detail_by_id(user_detail_id , data , db)

@user_detail_route.delete("/{user_detail_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_user_detail(user_detail_id:int , db:DB):
    await delete_user_detail_by_id(user_detail_id, db)