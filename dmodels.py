from __future__ import annotations
from typing import List, Optional
from sqlalchemy import (
    Integer, String, Boolean, Text, ForeignKey, DateTime, SmallInteger, UniqueConstraint,
    Table, func, Column, sql, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import EmailStr

class Base(DeclarativeBase):
    pass


role_permission = Table(
    "role_permissions",
    Base.metadata,
    Column("role_name", String(30), ForeignKey("roles.role_name", ondelete="CASCADE"), primary_key=True, autoincrement=False),
    Column("permission_name", String(30), ForeignKey("permissions.permission_name", ondelete="CASCADE"), primary_key=True, autoincrement=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)


class Role(Base):
    __tablename__ = "roles"
    role_name: Mapped[str] = mapped_column(String(30), primary_key=True, autoincrement=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    permissions: Mapped[List[Permission]] = relationship(
        "Permission", 
        back_populates="roles", 
        secondary=role_permission,
        passive_deletes=True)
    users: Mapped[List[User]] = relationship("User", back_populates="role")



class Permission(Base):
    __tablename__ = "permissions"
    permission_name: Mapped[str] = mapped_column(String(30), primary_key=True, autoincrement=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    roles: Mapped[List[Role]] = relationship(
        "Role", 
        back_populates="permissions",
        secondary=role_permission, 
        passive_deletes=True)



class Department(Base):
    __tablename__ = "departments"
    department_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_name: Mapped[str] = mapped_column(String(30), nullable=False, unique= True)
    department_code: Mapped[str] = mapped_column(String(30), nullable=False, unique= True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    semesters: Mapped[List[Semester]] = relationship("Semester", back_populates="department")
    assignments: Mapped[List[Assignment]] = relationship("Assignment", back_populates="department")
    teacher_announcements:Mapped[List["TeacherAnnouncement"]] = relationship("TeacherAnnouncement" ,back_populates="department")



class Semester(Base):
    __tablename__ = "semesters"
    __table_args__ = (
        UniqueConstraint("department_id", "semester_name", name="uq_department_section"),
    )
    semester_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    semester_name: Mapped[str] = mapped_column(String(50), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.department_id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    department: Mapped[Department] = relationship("Department", back_populates="semesters")
    sections: Mapped[List[Section]] = relationship("Section", back_populates="semester")
    subjects: Mapped[List[Subject]] = relationship("Subject", back_populates="semester")



class Section(Base):
    __tablename__ = "sections"
    __table_args__ = (
        UniqueConstraint("semester_id", "section_name", name="uq_semester_section"),
    )
    section_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_name: Mapped[str] = mapped_column(String(5), nullable=False)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.semester_id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    semester: Mapped[Semester] = relationship("Semester", back_populates="sections")
    teaching_assignments: Mapped[List[TeachingAssignment]] = relationship("TeachingAssignment", back_populates="section")
    assignments: Mapped[List[Assignment]] = relationship("Assignment", back_populates="section")
    teacher_announcements:Mapped[List["TeacherAnnouncement"]] = relationship("TeacherAnnouncement" ,back_populates="section")
    students:Mapped[List["Student"]] = relationship("Student", back_populates= "section")




class UserDetails(Base):
    __tablename__ = "user_details"
    __table_args__ = (
        CheckConstraint("age >= 0 AND age <= 150", name="valid_age_range"),
        CheckConstraint("gender IN ('male', 'female')", name="valid_gender_values"),
    )
    user_detail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, server_default=sql.expression.null())
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id", ondelete="RESTRICT"), nullable=False)
    ph_number: Mapped[str] = mapped_column(String(15), nullable=False)
    ph_number_extra: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="user_detail", uselist=False)
    address: Mapped["Address"] = relationship("Address", back_populates="userdetail")


class Address(Base):
    __tablename__ = "addresses"
    __table_args__ = (
    UniqueConstraint(
        "province_name", "district_name", "village_city_name", "ward_number", "place_name",
        name="uq_full_address"
    ),)

    address_id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    province_name: Mapped[str] = mapped_column(String(30), nullable=False, index= True)
    district_name: Mapped[str] = mapped_column(String(30), nullable=False, index= True)
    village_city_name: Mapped[str] = mapped_column(String(30), nullable=False, index= True)
    ward_number: Mapped[int] = mapped_column(SmallInteger, nullable=False, index= True)
    place_name: Mapped[str] = mapped_column(String(30), nullable=False, index= True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    userdetail: Mapped[List[UserDetails]] = relationship("UserDetails", back_populates="address")


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(ForeignKey("roles.role_name", ondelete="RESTRICT"), nullable=False)
    user_detail_id: Mapped[int] = mapped_column(ForeignKey("user_details.user_detail_id" , ondelete="RESTRICT"),
                                                 nullable=False,unique=True )
    email_id: Mapped[EmailStr] = mapped_column(String(50), nullable=False, unique=True)
    hashed_pw: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sql.expression.true())
    is_first_login: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sql.expression.true())
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    role: Mapped[Role] = relationship("Role", back_populates="users")
    user_detail: Mapped["UserDetails"] = relationship("UserDetails", back_populates="user")
    resources: Mapped[List[Resource]] = relationship("Resource", back_populates="user")
    admin: Mapped[Optional[Admin]] = relationship("Admin", back_populates="user", uselist=False)
    teacher: Mapped[Optional[Teacher]] = relationship("Teacher", back_populates="user", uselist=False)
    student: Mapped[Optional[Student]] = relationship("Student", back_populates="user", uselist=False)




class Resource(Base):
    __tablename__ = "resources"
    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    path: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped[User] = relationship("User", back_populates="resources")
    assignment_submissions: Mapped[List[AssignmentSubmission]] = relationship("AssignmentSubmission", back_populates="resource")
    subject: Mapped[Optional[Subject]] = relationship("Subject", back_populates="resource", uselist=False)




class Subject(Base):
    __tablename__ = "subjects"
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(30), nullable=False, unique= True)
    subject_code: Mapped[str] = mapped_column(String(10), nullable=False, unique= True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.semester_id"), nullable=False)
    resource_id: Mapped[Optional[int]] = mapped_column(ForeignKey("resources.resource_id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    semester: Mapped[Semester] = relationship("Semester", back_populates="subjects")
    teaching_assignments: Mapped[List[TeachingAssignment]] = relationship("TeachingAssignment", back_populates="subject")
    assignments: Mapped[List[Assignment]] = relationship("Assignment", back_populates="subject")
    resource: Mapped[Optional[Resource]] = relationship("Resource", back_populates="subject")
    teacher_announcements:Mapped[List["TeacherAnnouncement"]] = relationship("TeacherAnnouncement" ,back_populates="subject")




class Admin(Base):
    __tablename__ = "admins"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship("User", back_populates="admin")
    admin_announcements: Mapped[List["AdminAnnouncement"]] = relationship("AdminAnnouncement", back_populates="admin")





class Teacher(Base):
    __tablename__ = "teachers"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship("User", back_populates="teacher")
    teaching_assignments: Mapped[List[TeachingAssignment]] = relationship("TeachingAssignment", back_populates="teacher")
    assignments: Mapped[List[Assignment]] = relationship("Assignment", back_populates="teacher")
    teacher_announcements:Mapped[List["TeacherAnnouncement"]] = relationship("TeacherAnnouncement" ,back_populates="teacher")



class TeachingAssignment(Base):
    __tablename__ = "teaching_assignments"
    
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.user_id"), primary_key=True, autoincrement=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), primary_key=True, autoincrement=False)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.section_id"), primary_key=True, autoincrement=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="teaching_assignments")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="teaching_assignments")
    section: Mapped["Section"] = relationship("Section", back_populates="teaching_assignments")

    def __repr__(self):
        return (f"<TeachingAssignment(teacher_id={self.teacher_id}, "
                f"subject_id={self.subject_id}, section_id={self.section_id})>")




class Student(Base):
    __tablename__ = "students"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"), primary_key=True)
    batch_name:Mapped[str] = mapped_column(String(10), nullable= False , index= True)
    section_id:Mapped[int] = mapped_column(ForeignKey("sections.section_id", ondelete="RESTRICT"))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="student")
    section: Mapped["Section"] = relationship("Section", back_populates="students")
    assignment_submissions: Mapped[List[AssignmentSubmission]] = relationship("AssignmentSubmission", back_populates="student")



class Assignment(Base):
    __tablename__ = "assignments"
    assignment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.user_id"), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.department_id"), nullable=False)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.section_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"),  nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    deadline_time:Mapped[Optional[str]] = mapped_column(String(30), nullable= True)
    has_deadline_reached:Mapped[Optional[bool]] = mapped_column(Boolean , server_default= sql.expression.false())
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    teacher: Mapped[Teacher] = relationship("Teacher", back_populates="assignments")
    department: Mapped[Department] = relationship("Department", back_populates="assignments")
    section: Mapped[Section] = relationship("Section", back_populates="assignments")
    subject: Mapped[Subject] = relationship("Subject", back_populates="assignments")
    assignment_submissions: Mapped[List[AssignmentSubmission]] = relationship("AssignmentSubmission", back_populates="assignment")




class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    assignment_submission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.assignment_id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.resource_id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    assignment: Mapped[Assignment] = relationship("Assignment", back_populates="assignment_submissions")
    student: Mapped[Student] = relationship("Student", back_populates="assignment_submissions")
    resource: Mapped[Resource] = relationship("Resource", back_populates="assignment_submissions")




class AdminAnnouncement(Base):
    __tablename__ = "admin_announcements" 
    admin_announcement_id:Mapped[int] = mapped_column(Integer, primary_key= True)
    admin_id:Mapped[int] = mapped_column(ForeignKey("admins.user_id"),nullable= False)
    title:Mapped[str] = mapped_column(String(30),nullable= False)
    description:Mapped[str] = mapped_column(Text,nullable= False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    admin: Mapped["Admin"] = relationship("Admin", back_populates="admin_announcements")




class TeacherAnnouncement(Base):
    __tablename__ = "teacher_announcements" 
    teacher_announcement_id:Mapped[int] = mapped_column(Integer, primary_key= True)
    teacher_id:Mapped[int] = mapped_column(ForeignKey("teachers.user_id"),nullable= False)
    department_id:Mapped[int] = mapped_column(ForeignKey("departments.department_id"),nullable= False)
    section_id:Mapped[int] = mapped_column(ForeignKey("sections.section_id"),nullable= False)
    subject_id:Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"),nullable= False)
    title:Mapped[str] = mapped_column(String(30),nullable= False)
    description:Mapped[str] = mapped_column(Text,nullable= False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="teacher_announcements")
    department: Mapped["Department"] = relationship("Department", back_populates="teacher_announcements")
    section: Mapped["Section"] = relationship("Section", back_populates="teacher_announcements")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="teacher_announcements")
