from fastapi import APIRouter, status , HTTPException
from database import DB
from auth.cryptography import Form_Data,create_access_token,create_refresh_token
from .helper import authenticate_user
from .model import ReturnMessage
from .crud import handle_first_login
from custom_http_error import CustomHttpError,HttpErrorMessages
login_route = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@login_route.post("/", status_code=status.HTTP_200_OK, response_model=ReturnMessage)
async def login(form_data: Form_Data, db: DB):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise CustomHttpError.NotFound_404(HttpErrorMessages.USER_NOT_FOUND_404)
    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(user.user_id)
    first_login:bool = await handle_first_login(user,db)
    return ReturnMessage(
        access_token=access_token,
        refresh_token=refresh_token,
        is_first_login= first_login,
        message="Login Successful",
        role=user.role_name
    )
