from typing import List

from sqlalchemy import String, Integer, Enum, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..schemas import Role
from .base_model import Base
from .bookings_model import Booking


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(BigInteger)
    role: Mapped['Role'] = mapped_column(Enum(Role))
    acc_status: Mapped[bool] = mapped_column(Boolean)

    bookings: Mapped[List['Booking']] = relationship(
        'Booking', back_populates='user'
    )
