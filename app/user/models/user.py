from sqlalchemy import Column, Unicode, BigInteger, Boolean
from sqlalchemy.orm import relationship
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    username = Column(Unicode(255), nullable=True, unique=True)
    is_admin = Column(Boolean, default=False)

    service_permission = relationship("ServicePermission", back_populates="user", lazy=True)


class Role(Base, TimestampMixin):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(Unicode(255), nullable=False)

    service_permission = relationship("ServicePermission", back_populates="role", lazy=True)
