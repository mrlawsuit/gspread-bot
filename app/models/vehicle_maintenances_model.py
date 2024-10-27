from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..schemas import MaintenanceStatus
from .base_model import Base
if TYPE_CHECKING:
    from .services_model import Service


class VehicleMaintenance(Base):
    __tablename__ = 'maintenances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('vehicles.id', ondelete='CASCADE')
    )
    workshop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('workshops.id', ondelete='CASCADE')
    )
    service_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    current_mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped['MaintenanceStatus'] = mapped_column(
        Enum(MaintenanceStatus)
    )

    services: Mapped['Service'] = relationship(
        'Service',
        secondary='maintenances_services',
        back_populates='maintenances'
    )