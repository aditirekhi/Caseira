from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

Model = TypeVar("Model", bound=SQLModel)


class BaseService(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        print("-------------------------------- Entering BaseService.__init__")
        self.model: type[Model] = model
        self.session = session

    async def _get(self, id: UUID) -> Model | None:
        print("-------------------------------- Entering BaseService._get")
        return await self.session.get(self.model, id)

    async def _exists(self, **filters: Any) -> bool:
        print("-------------------------------- Entering BaseService._exists")
        statement = select(self.model)
        for field_name, value in filters.items():
            statement = statement.where(getattr(self.model, field_name) == value)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def _create(self, data: Model) -> Model:
        print("-------------------------------- Entering BaseService._create")
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def _update(self, data: Model) -> Model:
        print("-------------------------------- Entering BaseService._update")
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def _delete(self, data: Model) -> Model:
        print("-------------------------------- Entering BaseService._delete")
        await self.session.delete(data)
        await self.session.commit()
        return data
