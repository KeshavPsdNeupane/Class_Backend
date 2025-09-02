from fastapi import APIRouter, HTTPException, status 
from jose import jwt, JWTError, ExpiredSignatureError
from database import DB
from custom_http_error import CustomHttpError,HttpErrorMessages
from auth.cryptography import (
    create_access_token, 
    REFRESH_SECRET_KEY,
    ALGORITHM
)
from .model import RefreshTokenRequest, ReturnMessage
from ..user_login.crud import get_user_with_id

refresh_router = APIRouter(prefix="/token/refresh", tags=["Token Refresh"])

@refresh_router.post("/", response_model=ReturnMessage)
async def refresh_token(request: RefreshTokenRequest, db: DB):
    credentials_exception = CustomHttpError.Unauthorized_401(HttpErrorMessages.INVALID_CREDENTIAL_UN_AUTH_401)
    try:
        payload = jwt.decode(request.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise CustomHttpError.Unauthorized_401(HttpErrorMessages.REFRESH_TOKEN_EXPIRED_UN_AUTH_401)
    except JWTError:
        raise CustomHttpError.Unauthorized_401(HttpErrorMessages.REFRESH_TOKEN_INVALID_UN_AUTH_401)
    except HTTPException as e:
        raise CustomHttpError.InternalServerError_500(f"Internal Server Error {str(e)}")
    user = await get_user_with_id(int(user_id), db)
    if not user:
        raise credentials_exception
    access_token = create_access_token(user.user_id)
    return ReturnMessage(
        access_token=access_token,
        token_type="bearer",
        message="Token refreshed successfully",
    )
