from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, Enum, FLOAT, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from ..schemas import BookingStatus


if TYPE_CHECKING:
    from .users_model import User
    from .vehicles_model import Vehicle


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('vehicles.id', ondelete='CASCADE')
    )
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus))
    price: Mapped[float] = mapped_column(FLOAT)

    user: Mapped['User'] = relationship('User', back_populates='bookings')
    vehicle: Mapped['Vehicle'] = relationship(
        'Vehicle', back_populates='bookings'
    )