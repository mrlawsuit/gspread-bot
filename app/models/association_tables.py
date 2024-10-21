from sqlalchemy import Integer, ForeignKey, Table, Column
from .base_model import Base

# вспомагательные таблицы
# многие ко многим services <-> maintenance
maintenances_services = Table(
    'maintenance_services',
    Base.metadata,
    Column(
        'maintenance_id',
        Integer,
        ForeignKey('maintenance.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'service_id',
        Integer,
        ForeignKey('services.id', ondelete='CASCADE'),
        primary_key=True
    )
)


# многие ко многим services <-> workshops
workshops_services = Table(
    'workshops_services',
    Base.metadata,
    Column(
        'workshop_id',
        Integer,
        ForeignKey('workshops.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'service_id',
        Integer,
        ForeignKey('services.id', ondelete='CASCADE'),
        primary_key=True
    )
)
