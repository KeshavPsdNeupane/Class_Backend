from fastapi import APIRouter
from .getUser import (
         Admin_Scope,
        Teacher_Scope ,
        Student_Scope,
        Admin_Teacher_Scope,
        Admin_Student_Scope,
        Teacher_Student_Scope,
        Any_Role_Scope
        )
from .user_register import user_register_route
from .user_login import login_route
from .password_change import password_change_route
from .user_refresh.user_refresh import refresh_router



auth_route = APIRouter(
    prefix= "/auth"
)


auth_route.include_router(user_register_route)
auth_route.include_router(login_route)
auth_route.include_router(password_change_route)
auth_route.include_router(refresh_router)


