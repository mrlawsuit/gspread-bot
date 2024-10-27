from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .workshops_model import Workshop
from .vehicle_maintenances_model import VehicleMaintenance
from .association_tables import workshops_services, maintenances_services


class Service(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)

    maintenances: Mapped['VehicleMaintenance'] = relationship(
        'VehicleMaintenance',
        secondary='maintenances_services',
        back_populates='services'
    )
    workshops: Mapped['Workshop'] = relationship(
        'Workshop',
        secondary='workshops_services',
        back_populates='services'
    )
