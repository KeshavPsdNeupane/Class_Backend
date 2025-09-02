from database import DB
from dmodels import User
from fastapi import  Security
from fastapi.security import  SecurityScopes
from typing import Annotated
from jose import jwt, JWTError, ExpiredSignatureError
from .cryptography import (
    Token,
    SECRET_KEY,
    ALGORITHM,
)
from custom_http_error import CustomHttpError,HttpErrorMessages
from .user_login.crud import get_user_with_id

async def get_current_user(
        security_scopes: SecurityScopes,token: Token,db: DB) -> User:
    credentials_error = CustomHttpError.Unauthorized_401(HttpErrorMessages.INVALID_CREDENTIAL_UN_AUTH_401)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise 
    except ExpiredSignatureError:
        raise CustomHttpError.Unauthorized_401(HttpErrorMessages.ACCESS_TOKEN_EXPIRED_UN_AUTH_401)
    except JWTError:
        raise CustomHttpError.Unauthorized_401(HttpErrorMessages.ACCESS_TOKEN_INVALID_UN_AUTH_401)
    user = await get_user_with_id(user_id, db)
    if not user:
        raise credentials_error

    if security_scopes.scopes:
        if user.role_name not in security_scopes.scopes:
            raise CustomHttpError.Forbidden_403(HttpErrorMessages.INVALID_ROLE_FORBIDDEN_403(user.role_name))
    return user

Admin_Scope = Annotated[User, Security(get_current_user, scopes=["admin"])]
Teacher_Scope = Annotated[User, Security(get_current_user, scopes=["teacher"])]
Student_Scope = Annotated[User, Security(get_current_user, scopes=["student"])]
Admin_Teacher_Scope = Annotated[User, Security(get_current_user, scopes=["admin", "teacher"])]
Admin_Student_Scope = Annotated[User, Security(get_current_user, scopes=["admin", "student"])]
Teacher_Student_Scope = Annotated[User, Security(get_current_user, scopes=["teacher", "student"])]
Any_Role_Scope = Annotated[User, Security(get_current_user, scopes=["admin", "teacher", "student"])]
