from fastapi import APIRouter , status
from database import DB
from .model import PasswordChange,Respone
from .crud import password_change
from auth.getUser import Any_Role_Scope

password_change_route = APIRouter(
    prefix="/password_change",
    tags=["Password Change"]
)


@password_change_route.post("/", status_code=status.HTTP_200_OK,response_model=Respone)
async def change_password(user:Any_Role_Scope , data:PasswordChange , db:DB):
    await password_change(user, data, db)
    return Respone(message="Password Changed Successfully")
