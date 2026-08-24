from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import CategoryDetails
from schemas.category import CategoryClassCreate, CategoryClassRead, CategoryClassUpdate
from services.base import BaseService


class CategoryService(BaseService[CategoryDetails]):
    def __init__(self, session):
        super().__init__(CategoryDetails, session)

    async def fetch_all_categories(self) -> list[CategoryClassRead]:
        print(
            "-------------------------------- Entering CategoryService.fetch_all_categories"
        )
        statement = select(self.model).order_by(self.model.category_name)

        categories = await self.session.execute(statement)

        rows = categories.scalars().all()

        if rows is None:
            return []
        else:
            return [
                CategoryClassRead(
                    category_id=row.category_id,
                    category_name=row.category_name,
                    category_description=row.category_description,
                    image_url=row.image_url,
                    recipes_count=len(row.recipes),
                )
                for row in rows
                if row.category_id
            ]

    async def fetch_category_by_id(self, category_id: UUID):
        print(
            "-------------------------------- Entering CategoryService.fetch_category_by_id"
        )
        category = await self._get(category_id)

        if category is None:
            return None
        else:
            return category

    async def create_category(self, payload: CategoryClassCreate, username: str):
        print(
            "-------------------------------- Entering CategoryService.create_category"
        )

        category_name_exists = await self.check_category_name_exists(
            payload.category_name
        )

        if category_name_exists:
            return None
        else:
            category = self.model(
                category_name=payload.category_name,
                category_description=payload.category_description,
                image_url=payload.image_url,
                created_by=username,
            )

            category_created = await self._create(category)
            return category_created

    async def update_category(
        self, category_id: UUID, payload: CategoryClassUpdate, userName: str
    ):
        print(
            "-------------------------------- Entering CategoryService.update_category"
        )

        category = await self._get(category_id)

        if category is None:
            return None
        else:
            category.category_name = payload.category_name or category.category_name
            category.category_description = (
                payload.category_description or category.category_description
            )
            category.image_url = payload.image_url or category.image_url
            category.created_by = userName

            category_updated = await self._update(category)
            return category_updated

    async def delete_category(self, category_id: UUID):
        print(
            "-------------------------------- Entering CategoryService.delete_category"
        )

        category = await self._get(category_id)

        if category is None:
            return None
        else:
            category_deleted = await self._delete(category)
            return category_deleted

    async def check_category_name_exists(self, category_name: str):
        print(
            "-------------------------------- Entering CategoryService.check_category_name_exists"
        )

        model = cast(Any, self.model)
        statement = select(model).where(model.category_name == category_name)

        category = await self.session.execute(statement)
        category = category.scalar_one_or_none()

        return category

    async def get_category_id_by_name(self, category_name: str):
        print(
            "-------------------------------- Entering CategoryService.get_category_id_by_name"
        )

        model = cast(Any, self.model)

        statement = select(model.category_id).where(
            model.category_name == category_name
        )

        category_id = await self.session.execute(statement)

        if category_id is None:
            return None
        else:
            return category_id.scalar_one_or_none()
