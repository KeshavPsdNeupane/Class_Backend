from database import DB
from .crud import get_user_by_email
from pydantic import EmailStr
from auth.cryptography import verify_password


async def authenticate_user(email_id:EmailStr , password:str , db:DB):
    user = await get_user_by_email(email_id, db)
    if not user:
        return False
    if not verify_password(password , user.hashed_pw):
        return False
    return user

