from typing import List

from fastapi import APIRouter, Depends, Query, Response, Request

from api.user.v1.request.user import LoginRequest
from api.user.v1.response.user import LoginResponse
from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserResponseSchema,
    CreateUserRequestSchema,
    DeleteUserRequestSchema,
    UpdateUserResponseSchema,
    AddUserPermissionRequestSchema,
    CreateRoleRequestSchema
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
    AllowAll
)

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"password"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)

@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(**request.dict())

    return {"email": request.email, "username": request.username}


@user_router.delete(
    "",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def delete_user_by_email(request: DeleteUserRequestSchema):
    await UserService().delete_user_by_email(**request.dict())

    return Response(status_code=200)

@user_router.put(
    "",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def update_user_username(request: UpdateUserResponseSchema):
    await UserService().update_user_username(**request.dict())

    return Response(status_code=200)


@user_router.post(
    "/login",
    response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def login(request: LoginRequest):
    token = await UserService().login(**request.dict())

    return {"token": token.token, "refresh_token": token.refresh_token}

@user_router.post(
    "/role",
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def create_role(request: CreateRoleRequestSchema):
    await UserService().create_role(**request.dict())

    return Response(status_code=200)
