from sqlalchemy import String, Integer, Enum as SQLEnum, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..schemas import CarStatus
from .base_model import Base
from .bookings_model import Booking


class Vehicle(Base):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(128))
    release: Mapped[int] = mapped_column(Integer)
    plate: Mapped[str] = mapped_column(String(65))
    mileage: Mapped[float] = mapped_column(FLOAT)
    status: Mapped['CarStatus'] = mapped_column(SQLEnum(CarStatus))

    bookings: Mapped['Booking'] = relationship(
        'Booking',
        back_populates='vehicle'
    )
