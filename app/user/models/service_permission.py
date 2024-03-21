from sqlalchemy import Column, Unicode, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from core.db.mixins import TimestampMixin


class ServicePermission(Base, TimestampMixin):
    __tablename__ = "service_permission"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, ForeignKey('user.id'))
    role_id = Column(BigInteger, ForeignKey('role.id'))
    service_id = Column(BigInteger, ForeignKey('service.id'))

    user = relationship("User", back_populates="service_permission", lazy=True)
    role = relationship("Role", back_populates="service_permission", lazy=True)
    service = relationship("Service", back_populates="service_permission", lazy=True)


