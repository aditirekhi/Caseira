from typing import Any, cast
from uuid import UUID

from sqlalchemy.future import select

from database.models import UserCalendarPlanDetails
from schemas.user_calendar_plan_details import (
    UserCalendarPlanDetailsCreate,
    UserCalendarPlanDetailsRead,
)
from services.base import BaseService


class UserCalendarPlanDetailsService(BaseService[UserCalendarPlanDetails]):
    def __init__(self, session):
        super().__init__(UserCalendarPlanDetails, session)

    async def fetch_user_calendar_plan_details_by_user_id(
        self, user_id: UUID
    ) -> list[UserCalendarPlanDetailsRead]:
        print(
            "-------------------------------- Entering UserCalendarPlanDetailsService.fetch_user_calendar_plan_details_by_user_id"
        )

        from services.recipes import RecipesService

        recipe_service = RecipesService(self.session)

        model = cast(Any, self.model)
        query = select(model).where(model.user_id == user_id)

        result = await self.session.execute(query)

        rows = result.scalars().all()
        if not rows:
            return []

        plan_details: list[UserCalendarPlanDetailsRead] = []
        for row in rows:
            recipe = await recipe_service.fetch_recipe_by_id(row.recipe_id)
            if recipe is None:
                continue

            plan_details.append(
                UserCalendarPlanDetailsRead(
                    user_calendar_plan_id=row.user_calendar_plan_id,
                    user_id=row.user_id,
                    recipe_id=row.recipe_id,
                    recipe_name=recipe.recipe_name,
                    plan_date=row.plan_date,
                )
            )

        return plan_details

    async def fetch_user_calendar_plan_details_by_user_id_recipe_id(
        self, user_id: UUID, recipe_id: UUID
    ) -> UserCalendarPlanDetailsRead | None:
        print(
            "-------------------------------- Entering UserCalendarPlanDetailsService.fetch_user_calendar_plan_details_by_user_id_recipe_id"
        )

        from services.recipes import RecipesService

        recipe_service = RecipesService(self.session)

        model = cast(Any, self.model)
        query = (
            select(model)
            .where(model.user_id == user_id, model.recipe_id == recipe_id)
            .limit(1)
        )

        result = await self.session.execute(query)
        row = result.scalars().first()

        if not row:
            return None
        recipe = await recipe_service.fetch_recipe_by_id(row.recipe_id)
        if recipe is None:
            return None
        return UserCalendarPlanDetailsRead(
            user_calendar_plan_id=row.user_calendar_plan_id,
            user_id=row.user_id,
            recipe_id=row.recipe_id,
            recipe_name=recipe.recipe_name,
            plan_date=row.plan_date,
        )

    async def create_new_user_calendar_plan(
        self, payload: UserCalendarPlanDetailsCreate, user_id: UUID, username: str
    ) -> UserCalendarPlanDetailsRead | None:
        print(
            "-------------------------------- Entering UserCalendarPlanDetailsService.create_new_user_calendar_plan"
        )

        new_user_calendar_plan = (
            await self.fetch_user_calendar_plan_details_by_user_id_recipe_id(
                user_id, payload.recipe_id
            )
        )

        if new_user_calendar_plan:
            return await self.update_calendar_plan(payload, user_id)
        else:
            from services.recipes import RecipesService

            recipe_service = RecipesService(self.session)

            new_user_calendar_plan = UserCalendarPlanDetails(
                user_id=user_id,
                recipe_id=payload.recipe_id,
                plan_date=payload.plan_date,
                created_by=username,
            )

            result = await self._create(new_user_calendar_plan)
            recipe = await recipe_service.fetch_recipe_by_id(
                result.recipe_id or UUID(int=0)
            )
            if recipe is None:
                return None

            return UserCalendarPlanDetailsRead(
                user_calendar_plan_id=result.user_calendar_plan_id or UUID(int=0),
                user_id=result.user_id or UUID(int=0),
                recipe_id=result.recipe_id or UUID(int=0),
                recipe_name=recipe.recipe_name,
                plan_date=result.plan_date,
            )

    async def update_calendar_plan(
        self, payload: UserCalendarPlanDetailsCreate, user_id: UUID
    ) -> UserCalendarPlanDetailsRead | None:
        print(
            "-------------------------------- Entering UserCalendarPlanDetailsService.update_calendar_plan"
        )

        model = cast(Any, self.model)
        query = (
            select(model)
            .where(model.user_id == user_id, model.recipe_id == payload.recipe_id)
            .limit(1)
        )
        result = await self.session.execute(query)
        existing_plan = result.scalars().first()

        if not existing_plan:
            return None

        existing_plan.plan_date = payload.plan_date
        updated_plan = await self._update(existing_plan)

        from services.recipes import RecipesService

        recipe_service = RecipesService(self.session)
        recipe = await recipe_service.fetch_recipe_by_id(
            updated_plan.recipe_id or UUID(int=0)
        )
        if recipe is None:
            return None

        return UserCalendarPlanDetailsRead(
            user_calendar_plan_id=updated_plan.user_calendar_plan_id or UUID(int=0),
            user_id=updated_plan.user_id or UUID(int=0),
            recipe_id=updated_plan.recipe_id or UUID(int=0),
            recipe_name=recipe.recipe_name,
            plan_date=updated_plan.plan_date,
        )

    async def delete_calendar_plan(
        self, user_calendar_plan_details_id: UUID
    ) -> UserCalendarPlanDetailsRead | None:
        print(
            "-------------------------------- Entering UserCalendarPlanDetailsService.delete_calendar_plan"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            model.user_calendar_plan_id == user_calendar_plan_details_id
        )

        result = await self.session.execute(query)
        row = result.scalars().first()

        if not row:
            return None
        else:
            deleted_plan = await self._delete(row)

            from services.recipes import RecipesService

            recipe_service = RecipesService(self.session)
            recipe = await recipe_service.fetch_recipe_by_id(
                deleted_plan.recipe_id or UUID(int=0)
            )
            if recipe is None:
                return None

            return UserCalendarPlanDetailsRead(
                user_calendar_plan_id=deleted_plan.user_calendar_plan_id or UUID(int=0),
                user_id=deleted_plan.user_id or UUID(int=0),
                recipe_id=deleted_plan.recipe_id or UUID(int=0),
                recipe_name=recipe.recipe_name,
                plan_date=deleted_plan.plan_date,
            )
