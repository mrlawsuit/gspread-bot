from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Enum, Boolean, BigInteger, FLOAT, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.schemas import Role, CarStatus, BookingStatus, MaintainceStatus


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(BigInteger)
    role: Mapped['Role'] = mapped_column(Enum(Role))
    acc_status: Mapped[bool] = mapped_column(Boolean)

    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='user')


class Vehicle(Base):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(128))
    release: Mapped[int] = mapped_column(Integer)
    plate: Mapped[str] = mapped_column(String(65))
    mileage: Mapped[float] = mapped_column(FLOAT)
    status: Mapped['CarStatus'] = mapped_column(Enum(CarStatus))

    bookings: Mapped['Booking'] = relationship('Booking', back_populates='bookings')


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus))
    price: Mapped[float] = mapped_column(FLOAT)

    user: Mapped['User'] = relationship('User', back_populates='bookings')
    vehicle: Mapped['Vehicle'] = relationship('Vehicle', back_populates='vehicles')


class Service(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)
    
    maintainces: Mapped['VehicleMaintaince'] = relationship('VehicleMaintaince', secondary='maintaince_services', back_populates='services')


class Workshop(Base):
    __tablename__ = 'workshops'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    adress: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(BigInteger)
    # service_list: Mapped[str] = mapped_column(String(255), ForeignKey('services.id', ondelete='CASCADE'))

    services: Mapped['Service'] = relationship('Service', secondary='maintaince_services', back_populates='maintainces')
    

class VehicleMaintaince(Base):
    __tablename__ = 'maintainces'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'))
    workshop_id: Mapped[int] = mapped_column(Integer, ForeignKey('workshops.id', ondelete='CASCADE'))
    service_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped['MaintainceStatus'] = mapped_column(Enum(MaintainceStatus))

    services: Mapped['Service'] = relationship('Service', secondary='maintaince_services', back_populates='maintainces')

# services: Mapped['Service'] = relationship('Service', secondary='maintaince_services', back_populates='maintainces')

# вспомагательные таблицы
# многие ко многим services <-> maintaince
maintainces_services = Table(
    'maintaince_services',
    Base.metadata,
    Column('maintance_id', Integer, ForeignKey('maintainces.id', ondelete='CASCADE'), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id', ondelete='CASCADE'), primary_key=True)
)


# многие ко многим services <-> workshops
workshops_services = Table(
    'workshops_services',
    Base.metadata,
    Column('workshop_id', Integer, ForeignKey('workshops.id', ondelete='CASCADE'), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id', ondelete='CASCADE'), primary_key=True)
)