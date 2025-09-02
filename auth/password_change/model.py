from pydantic import BaseModel, EmailStr


class PasswordChange(BaseModel):
    old_password:str
    new_password:str
    confirm_password:str


class Respone(BaseModel):
    message:str