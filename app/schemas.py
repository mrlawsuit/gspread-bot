from enum import Enum
from pydantic import BaseModel


class Role(Enum):
    admin = 'администратор'
    client = 'клиент'


class CarStatus(Enum):
    available = 'доступен'
    being_serviced = 'на обслуживании'
    reserved = 'забронирован'


class BookingStatus(Enum):
    active = 'активно'
    finished = 'завершено'
    canceled = 'отменено'


class MaintainceStatus(Enum):
    planned = 'запланированно'
    in_process = 'в процессе'
    done = 'завершено'