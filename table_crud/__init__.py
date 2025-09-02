from fastapi import APIRouter
from .roles import role_route
from .permission import permission_route
from .role_permission import role_permission_route
from .userdetail import user_detail_route
from .address import address_route
from .department import department_route
from .semester import semester_route
from .section import section_route
from .user import user_route
from .resource import resource_route
from .subject import subject_route
from .admin import admin_route
from .teacher import teacher_route
from .student import student_route
from .teachingassignment import teach_assign_route
from .assignment import assignment_route
from .assignmentsubmission import assign_sub_route
from .adminannouncement import admin_announcement_route
from .teacherannouncement import teach_announcement_route
basic_table_route = APIRouter(
    prefix="/basic"
)

basic_table_route.include_router(role_route)
basic_table_route.include_router(permission_route)
basic_table_route.include_router(role_permission_route)
basic_table_route.include_router(user_detail_route)
basic_table_route.include_router(address_route)
basic_table_route.include_router(department_route)
basic_table_route.include_router(semester_route)
basic_table_route.include_router(section_route)
basic_table_route.include_router(user_route)
basic_table_route.include_router(resource_route)
basic_table_route.include_router(subject_route)
basic_table_route.include_router(admin_route)
basic_table_route.include_router(teacher_route)
basic_table_route.include_router(student_route)
basic_table_route.include_router(teach_assign_route)
basic_table_route.include_router(assignment_route)
basic_table_route.include_router(assign_sub_route)
basic_table_route.include_router(admin_announcement_route)
basic_table_route.include_router(teach_announcement_route)


