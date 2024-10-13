from enum import Enum
from pydantic import BaseModel


class Role(Enum):
    admin = 'администратор'
    client = 'клиент'
