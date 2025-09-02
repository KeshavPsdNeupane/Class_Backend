from fastapi import APIRouter , status
from database import DB
from .model import UserCreate,UserRead,UserUpdate
from .crud import(
    get_users,
    get_user_by_id,
    create_new_user,
    update_user_by_id,
    delete_user_by_id
)

user_route = APIRouter(
    prefix="/User",
    tags=["User"]
)

@user_route.post("/", response_model= UserCreate)
async def create_user(data:UserCreate , db:DB):
    return await create_new_user(data , db)



@user_route.get("/" ,  response_model= list[UserRead])
async def read_users(db:DB):
    return await get_users(db)

@user_route.get("/{user_id}" , response_model= UserRead)
async def read_user(user_id:int , db:DB):
    return await get_user_by_id(user_id , db)

@user_route.put("/{user_id}" , response_model= UserUpdate)
async def update_user(user_id:int ,  data:UserUpdate,db:DB):
    return await update_user_by_id(user_id,data , db)


@user_route.delete("/{user_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int , db:DB):
    await delete_user_by_id(user_id , db)
