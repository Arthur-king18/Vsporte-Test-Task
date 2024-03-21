import ast

from typing import Optional, List

from sqlalchemy import or_, select, and_, delete, update

from app.user.models import User, ServicePermission, Role, Service
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from passlib.context import CryptContext
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailException,
    DuplicateUsernameException,
    UserNotFoundException,
    UserWrongPasswordException
)
from core.utils.token_helper import TokenHelper

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().all()

    @Transactional()
    async def create_user(
            self,
            email: str,
            password1: str,
            password2: str,
            username: str,
            is_admin: bool = False
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(User.email == email)
        result = await session.execute(query)
        is_email_exist = result.scalars().first()

        if is_email_exist:
            raise DuplicateEmailException

        query = select(User).where(User.username == username)
        result = await session.execute(query)
        is_username_exist = result.scalars().first()

        if is_username_exist:
            raise DuplicateUsernameException

        user = User(email=email, password=pwd_context.hash(password1), username=username, is_admin=is_admin)

        session.add(user)

    @Transactional()
    async def create_service(
            self,
            name: str
    ) -> None:
        service = Service(name=name)

        session.add(service)

    @Transactional()
    async def delete_user_by_email(
            self,
            email: str
    ) -> None:
        query = delete(User).where(User.email == email)

        await session.execute(query)

    @Transactional()
    async def update_user_username(
            self,
            email: str,
            username: str
    ) -> None:
        query = update(User).where(User.email == email).values(username=username)

        await session.execute(query)

    @Transactional()
    async def add_permission_to_user(
            self,
            user_id: int,
            role_id: int,
            service_id: int
    ) -> None:
        service_permission = ServicePermission(
            user_id=user_id,
            role_id=role_id,
            service_id=service_id
        )

        session.add(service_permission)

    @Transactional()
    async def create_role(
            self,
            name: str
    ) -> None:
        role = Role(name=name)

        session.add(role)

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            return False

        return user.is_admin

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        if not self.verify_password(password, user.password):
            raise UserWrongPasswordException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}, expire_period=86400),  # 1 day
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}, expire_period=30 * 24 * 69 * 60),  # 30 days
        )

        return response

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)
