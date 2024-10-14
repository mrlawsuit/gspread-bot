from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Enum, Boolean, BigInteger, FLOAT, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from schemas import Role, CarStatus, BookingStatus, MaintainceStatus


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(BigInteger)
    role: Mapped[Role] = mapped_column(Enum(Role))
    acc_status: Mapped[bool] = mapped_column(Boolean)

    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="user")


class Vehicle(Base):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(128))
    release: Mapped[int] = mapped_column(Integer)
    plate: Mapped[str] = mapped_column(String(65))
    mileage: Mapped[float] = mapped_column(FLOAT)
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus))


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus))
    price: Mapped[float] = mapped_column(FLOAT)

    user: Mapped[User] = relationship("User", back_populates="bookings")



class Workshop(Base):
    __tablename__ = 'workshops'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    adress: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(BigInteger)
    service_list: Mapped[str] = mapped_column(String(255), ForeignKey('services.id', ondelete='CASCADE'))


class Service(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)


class VehicleMaintance(Base):
    __tablename__ = 'maintances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'))
    workshop_id: Mapped[int] = mapped_column(Integer, ForeignKey('workshops.id', ondelete='CASCADE'))
    service_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    service_list: Mapped[str] = mapped_column(String(255), ForeignKey('services.id', ondelete='CASCADE'))
    status: Mapped[MaintainceStatus] = mapped_column(Enum(MaintainceStatus))