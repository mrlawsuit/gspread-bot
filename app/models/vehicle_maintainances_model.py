from datetime import datetime

from sqlalchemy import Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schemas import MaintenanceStatus
from .base_model import Base
from .services_model import Service


class VehicleMaintenance(Base):
    __tablename__ = 'maintenance'
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
    status: Mapped['MaintenanceStatus'] = mapped_column(
        Enum(MaintenanceStatus)
    )

    services: Mapped['Service'] = relationship(
        'Service',
        secondary='maintenance_services',
        back_populates='maintenances'
    )
