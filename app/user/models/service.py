from sqlalchemy import Column, Unicode, BigInteger
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class Service(Base, TimestampMixin):
    __tablename__ = "service"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(Unicode(255), nullable=False)

    service_permission = relationship("ServicePermission", back_populates="service", lazy=True)


