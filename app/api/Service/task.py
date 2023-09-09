from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from .manager import BaseService
from db.db_structure import Task
from db.database import async_session_maker


class TaskService(BaseService):
    model = Task

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id, cls.model.title,
                                                               cls.model.description,
                                                               cls.model.completed)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception):
            return None
        
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            task = await cls.find_one_or_none(**filter_by)

            if not task:
                return None

            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            return task
        
    @classmethod
    async def update(cls, task_id, **filter_by):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(id=task_id).values(**filter_by)
            await session.execute(query)
            await session.commit()

            task = await cls.find_one_or_none(id=task_id)
            
            if not task:
                return None

            return task