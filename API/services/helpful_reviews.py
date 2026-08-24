from typing import Any, cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import HelpfulReviews
from schemas.helpful_review import (
    HelpfulReviewCreate,
    HelpfulReviewDelete,
    HelpfulReviewRead,
)
from services.base import BaseService


class HelpfulReviewsService(BaseService[HelpfulReviews]):
    def __init__(self, session: AsyncSession):
        super().__init__(HelpfulReviews, session)

    async def get_helpful_reviews_by_review_id(
        self, recipe_review_id: UUID
    ) -> list[HelpfulReviewRead] | None:
        print(
            "-------------------------------- Entering HelpfulReviewsService.get_helpful_reviews_by_review_id"
        )

        model = cast(Any, self.model)

        query = select(model).where(model.recipe_review_id == recipe_review_id)

        result = await self.session.execute(query)
        rows = result.scalars().all()

        if rows is None:
            return []
        return [HelpfulReviewRead(**helpful_review.__dict__) for helpful_review in rows]

    async def get_helpful_review_by_review_and_user_id(
        self, recipe_review_id: UUID, user_id: UUID
    ) -> HelpfulReviewRead | None:
        print(
            "-------------------------------- Entering HelpfulReviewsService.get_helpful_review_by_review_and_user_id"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            model.recipe_review_id == recipe_review_id, model.user_id == user_id
        )

        result = await self.session.execute(query)

        row = result.scalars().first()

        if row is None:
            return None
        return HelpfulReviewRead(**row.__dict__)

    async def create_helpful_review(
        self, helpful_review: HelpfulReviewCreate, user_id: UUID, username: str
    ) -> HelpfulReviewRead:
        print(
            "-------------------------------- Entering HelpfulReviewsService.create_helpful_review"
        )

        model = cast(Any, self.model)

        query = select(model).where(
            model.recipe_review_id == helpful_review.recipe_review_id,
            model.user_id == user_id,
        )

        existing_review = await self.session.execute(query)
        existing_review_instance = existing_review.scalars().first()

        if existing_review_instance is not None:
            return HelpfulReviewRead(
                helpful_review_id=existing_review_instance.helpful_review_id,
                recipe_review_id=existing_review_instance.recipe_review_id,
                user_id=existing_review_instance.user_id,
            )

        new_helpful_review = self.model(
            recipe_review_id=helpful_review.recipe_review_id,
            user_id=user_id,
            created_by=username,
        )

        result = await self._create(new_helpful_review)
        return HelpfulReviewRead(
            helpful_review_id=result.helpful_review_id or UUID(int=0),
            recipe_review_id=result.recipe_review_id or UUID(int=0),
            user_id=result.user_id or UUID(int=0),
        )

    # async def update_helpful_review(
    #     self, helpful_review: HelpfulReviewCreate, user_id: UUID, username: str
    # ) -> HelpfulReviewRead:
    #     print(
    #         "-------------------------------- Entering HelpfulReviewsService.update_helpful_review"
    #     )

    #     model = cast(Any, self.model)

    #     query = select(model).where(
    #         model.recipe_review_id == helpful_review.recipe_review_id,
    #         model.user_id == user_id,
    #     )

    #     existing_review = await self.session.execute(query)
    #     existing_review_instance = existing_review.scalars().first()

    #     if existing_review_instance is None:
    #         return await self.create_helpful_review(helpful_review, user_id, username)

    #     existing_review_instance.recipe_review_id = helpful_review.recipe_review_id
    #     existing_review_instance.user_id = user_id

    #     result = await self._update(existing_review_instance)
    #     return HelpfulReviewRead(
    #         helpful_review_id=result.helpful_review_id or UUID(int=0),
    #         recipe_review_id=result.recipe_review_id or UUID(int=0),
    #         user_id=result.user_id or UUID(int=0),
    #     )

    async def delete_helpful_review(
        self, helpful_review: HelpfulReviewDelete, user_id: UUID
    ) -> HelpfulReviewRead | None:
        print(
            "-------------------------------- Entering HelpfulReviewsService.delete_helpful_review"
        )

        model = cast(Any, self.model)

        query = select(model).where(
            model.recipe_review_id == helpful_review.recipe_review_id,
            model.user_id == user_id,
        )

        existing_review = await self.session.execute(query)
        existing_review_instance = existing_review.scalars().first()

        if existing_review_instance is None:
            return None

        result = await self._delete(existing_review_instance)
        return HelpfulReviewRead(**result.__dict__)
