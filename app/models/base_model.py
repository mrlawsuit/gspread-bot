from enum import Enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        return {c.name: self.enum_to_string(getattr(self, c.name)) for c in self.__table__.columns}    

    @staticmethod
    def enum_to_string(value):
        if isinstance(value, Enum):
            return value.value
        return value
