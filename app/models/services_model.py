from sqlalchemy import String, Integer, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .workshops_model import Workshop
from .vehicle_maintainances_model import VehicleMaintenance
from .association_tables import workshops_services, maintenance_services


class Service(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)

    maintenance: Mapped['VehicleMaintenance'] = relationship(
        'VehicleMaintenance',
        secondary=maintenance_services,
        back_populates='services'
    )
    workshops: Mapped['Workshop'] = relationship(
        'Workshop',
        secondary=workshops_services,
        back_populates='services'
    )
