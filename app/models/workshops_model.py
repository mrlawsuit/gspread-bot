from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .services_model import Service


class Workshop(Base):
    __tablename__ = 'workshops'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    adress: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(BigInteger)
    # service_list: Mapped[str] =
    # mapped_column(String(255), ForeignKey('services.id', ondelete='CASCADE'))

    services: Mapped['Service'] = relationship(
        'Service',
        secondary='workshops_services',
        back_populates='workshops'
    )
