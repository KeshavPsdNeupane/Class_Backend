from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from typing import Optional,Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import random
import string
from dotenv import load_dotenv
from project_util import getEnviromentVariable


load_dotenv()

pwd_context = CryptContext(schemes=["argon2"])



SECRET_KEY = getEnviromentVariable("SECRET_KEY")
REFRESH_SECRET_KEY=getEnviromentVariable("REFRESH_SECRET_KEY")
ALGORITHM = getEnviromentVariable("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 5
Form_Data = Annotated[OAuth2PasswordRequestForm, Depends()]

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scopes={
        "admin": "Administrator access",
        "teacher": "Teacher access",
        "student": "Student access"
    }
)
Token = Annotated[str, Depends(oauth_scheme)]


def get_hashed_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(password:str , hashed_pw:str)->bool:
    return pwd_context.verify(password , hashed_pw)


def create_password(length:int):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    print(random_string)
    return random_string


def create_access_token(user_id: int, expire_delta: Optional[timedelta] = None) -> str:
    to_encode: dict = {"sub": str(user_id)}
    expire = datetime.now(UTC) + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int, expire_delta: Optional[timedelta] = None) -> str:
    to_encode: dict = {"sub": str(user_id)}
    expire = datetime.now(UTC) + (expire_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt