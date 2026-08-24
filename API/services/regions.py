from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import RegionsDetails
from schemas.regions import RegionsClassCreate, RegionsClassRead, RegionsClassUpdate
from services.base import BaseService


class RegionsService(BaseService[RegionsDetails]):
    def __init__(self, session):
        print("-------------------------------- Entering RegionsService.__init__")
        super().__init__(RegionsDetails, session)

    async def fetch_all_regions(self) -> list[RegionsClassRead]:
        print(
            "-------------------------------- Entering RegionsService.fetch_all_regions"
        )

        statement = select(self.model).order_by(self.model.region_name)

        regions = await self.session.execute(statement)

        rows = regions.scalars().all()

        if rows is None:
            return []
        else:
            return [
                RegionsClassRead(
                    region_id=row.region_id,
                    region_name=row.region_name,
                    region_description=row.region_description,
                    image_url=row.image_url,
                    recipes_count=len(row.recipes),
                )
                for row in rows
                if row.region_id
            ]

    async def fetch_region_by_id(self, region_id: UUID):
        print(
            "-------------------------------- Entering RegionsService.fetch_region_by_id"
        )

        region = await self._get(region_id)

        if region is None:
            return None
        else:
            return region

    async def create_region(self, payload: RegionsClassCreate, username: str):
        print("-------------------------------- Entering RegionsService.create_region")

        region_name_exists = await self.check_region_name_exists(payload.region_name)

        if region_name_exists:
            return None
        else:
            region = self.model(
                region_name=payload.region_name,
                region_description=payload.region_description,
                created_by=username,
                image_url=payload.image_url,
            )

            region_created = await self._create(region)

            return region_created

    async def update_region(
        self, payload: RegionsClassUpdate, region_id: UUID, username: str
    ):
        print("-------------------------------- Entering RegionsService.update_region")

        region = await self._get(region_id)

        if region is None:
            return None
        else:
            region.region_name = payload.region_name or region.region_name
            region.region_description = (
                payload.region_description or region.region_description
            )
            region.image_url = payload.image_url or region.image_url
            region.created_by = username

            region_updated = await self._update(region)
            return region_updated

    async def delete_region(self, region_id: UUID):
        print("-------------------------------- Entering RegionsService.delete_region")

        region = await self._get(region_id)

        if region is None:
            return None
        else:
            region_deleted = await self._delete(region)

            print(region_deleted)

            return region_deleted

    async def check_region_name_exists(self, region_name: str):
        print(
            "-------------------------------- Entering RegionsService.check_region_name_exists"
        )

        model = cast(Any, self.model)
        statement = select(model).where(model.region_name == region_name)

        region = await self.session.execute(statement)
        region = region.scalar_one_or_none()

        return region

    async def get_region_id_by_name(self, region_name: str):
        print(
            "-------------------------------- Entering RegionsService.get_region_id_by_name"
        )

        model = cast(Any, self.model)
        statement = select(model.region_id).where(model.region_name == region_name)

        region_id = await self.session.execute(statement)

        if region_id is None:
            return None
        else:
            return region_id.scalar_one_or_none()
