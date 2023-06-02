from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import List, Dict

class UserBaseSchema(BaseModel):
    email: EmailStr
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=4)
    passwordConfirm: str
    verified: bool = False
    token: str = None
    first_name: str
    last_name: str
    email: str
    company_name:str
    credit: str
    profile_image: str
    resetPassword: str = None


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=4)


class UserResponseSchema(UserBaseSchema):
    id: str

class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class ForgetPassword(BaseModel):
    email: str


class ResetSchema(BaseModel):
    password: constr(min_length=4)
    passwordConfirm: str


