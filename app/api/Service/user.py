from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from .manager import BaseService
from db.db_structure import User
from db.database import async_session_maker


class UserService(BaseService):
    model = User

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id, cls.model.username,
                                                               cls.model.email)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception):
            return None