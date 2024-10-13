from sqlalchemy import String, Integer, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

from schemas import Role


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(Integer)
    role: Mapped[Role] = mapped_column(Enum(Role))
    acc_status: Mapped[bool] = mapped_column(Boolean)
