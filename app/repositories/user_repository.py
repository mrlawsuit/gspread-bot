from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import Role
from ..models import User
from ..database import async_session


async def get_admins_id() -> list:
    async with async_session() as session:
        result = await session.execute(
            select(User.id).
            where(
                User.role == Role.admin,
                User.acc_status
            )
        )
        admins_id = result.scalars().all()
    return admins_id


async def get_user_by_id_db(
        session: AsyncSession,
        id: int
):
    result = await session.execute(
        select(User).
        where(User.id == id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError('Нет такого пользователя')
    return user
