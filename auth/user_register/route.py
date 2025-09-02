from fastapi import APIRouter, status
from database import DB
from .model import UserCreateData,Respone
from .crud import(
    user_register
)


user_register_route = APIRouter(
    prefix="/register",
    tags=["User Register"]
)


@user_register_route.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(data: UserCreateData, db: DB):
    await user_register(data, db)
    return  Respone(message="User Registered Successfully")