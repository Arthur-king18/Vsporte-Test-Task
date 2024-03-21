from fastapi import APIRouter, Depends, Response

from app.user.schemas import (
    ExceptionResponseSchema,
    AddUserPermissionRequestSchema,
    CreateServiceRequestSchema
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin
)

service_router = APIRouter()


@service_router.post(
    "",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def create_service(request: CreateServiceRequestSchema):
    await UserService().create_service(**request.dict())

    return Response(status_code=200)


@service_router.post(
    "/add-permission",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def add_permission_to_user(request: AddUserPermissionRequestSchema):
    await UserService().add_permission_to_user(**request.dict())

    return Response(status_code=200)

