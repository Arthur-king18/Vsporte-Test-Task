import re
from pydantic import BaseModel, Field, validator

from core.exceptions import UserNotValidEmail


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")
    password: str = Field(..., description="Password")

    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1", min_length=6)
    password2: str = Field(..., description="Password2")
    username: str = Field(default="", description="Username")
    is_admin: bool = Field(default=False, description="Is Admin")

    @validator("email")
    def isValidEmail(cls, value: str) -> str:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, value):
            raise UserNotValidEmail
        return value


class CreateUserResponseSchema(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="Username")

    class Config:
        orm_mode = True

class UpdateUserResponseSchema(CreateUserResponseSchema):
    pass

class DeleteUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")

class AddUserPermissionRequestSchema(BaseModel):
    user_id: int = Field(..., description="User ID")
    role_id: int = Field(..., description="Role ID")
    service_id: int = Field(..., description="Service ID")


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")

class CreateRoleRequestSchema(BaseModel):
    name: str = Field(..., description="Name")

class CreateServiceRequestSchema(CreateRoleRequestSchema):
    pass



