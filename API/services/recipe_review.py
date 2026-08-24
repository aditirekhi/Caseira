from typing import Any, cast
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import HelpfulReviews, RecipeReviews, UserDetails
from schemas.recipe_reviews import (
    RecipeReviewRead,
    ReviewCreate,
    ReviewRead,
    ReviewUpdate,
)
from services.base import BaseService
from services.helpful_reviews import HelpfulReviewsService


class RecipeReviewsService(BaseService[RecipeReviews]):
    def __init__(self, session: AsyncSession):
        super().__init__(RecipeReviews, session)

    async def get_review_by_recipe_and_user_id(
        self, recipe_id: UUID, user_id: UUID
    ) -> list[ReviewRead] | None:
        print(
            "-------------------------------- Entering RecipeReviewsService.get_review_by_recipe_and_user_id"
        )

        model = cast(Any, self.model)
        statement = select(model)

        if recipe_id is not None:
            statement = statement.where(model.recipe_id == recipe_id)
        if user_id is not None:
            statement = statement.where(model.user_id == user_id)

        result = await self.session.execute(statement)

        if result is None:
            return []

        return [ReviewRead(**review.__dict__) for review in result.scalars().all()]

    async def get_all_reviews(self) -> list[ReviewRead] | None:
        print(
            "-------------------------------- Entering RecipeReviewsService.get_all_reviews"
        )

        model = cast(Any, self.model)
        statement = select(model)

        result = await self.session.execute(statement)

        if result is None:
            return []

        return [ReviewRead(**review.__dict__) for review in result.scalars().all()]

    async def get_review_by_recipe_id(self, recipe_id: UUID) -> RecipeReviewRead | None:
        print(
            "-------------------------------- Entering RecipeReviewsService.get_review_by_recipe_id"
        )

        helpful_reviews_service = HelpfulReviewsService(self.session)

        model = cast(Any, self.model)
        user_model = cast(Any, UserDetails)
        helpful_model = cast(Any, HelpfulReviews)

        statement = (
            select(
                model.recipe_review_id,
                model.user_id,
                model.recipe_id,
                model.comment,
                model.ratings,
                model.created_at,
                user_model.first_name,
                user_model.last_name,
                func.count(helpful_model.helpful_review_id).label(
                    "helpful_review_count"
                ),
            )
            .where(model.recipe_id == recipe_id)
            .join(user_model, model.user_id == user_model.user_id)
            .outerjoin(
                helpful_model,
                (helpful_model.recipe_review_id == model.recipe_review_id),
            )
            .group_by(
                model.recipe_review_id,
                model.user_id,
                model.recipe_id,
                model.comment,
                model.ratings,
                model.created_at,
                user_model.first_name,
                user_model.last_name,
            )
        )

        result = await self.session.execute(statement)

        rows = result.mappings().all()

        if not rows:
            return None
        total_review_count = len(rows)
        review_count_5 = 0
        review_count_4 = 0
        review_count_3 = 0
        review_count_2 = 0
        review_count_1 = 0
        overall_rating = 0
        avg_rating = 0.0

        reviews = []

        for row in rows:
            rating = row["ratings"]

            match rating:
                case rating if 4.5 <= rating <= 5:
                    review_count_5 += 1
                case rating if 3.5 <= rating < 4.5:
                    review_count_4 += 1
                case rating if 2.5 <= rating < 3.5:
                    review_count_3 += 1
                case rating if 1.5 <= rating < 2.5:
                    review_count_2 += 1
                case rating if 0.5 <= rating < 1.5:
                    review_count_1 += 1

            overall_rating += rating

            reviews.append(
                ReviewRead(
                    recipe_review_id=row["recipe_review_id"],
                    user_id=row["user_id"],
                    username=f"{row['first_name']} {row['last_name']}"
                    if row["first_name"] or row["last_name"]
                    else "Anonymous",
                    ratings=rating,
                    comment=row["comment"],
                    recipe_id=row["recipe_id"],
                    created_at=str(row["created_at"].strftime("%Y-%m-%d %H:%M:%S")),
                    helpful_review_count=row["helpful_review_count"],
                    helpful_review_given_by_user=bool(
                        await helpful_reviews_service.get_helpful_review_by_review_and_user_id(
                            recipe_review_id=row["recipe_review_id"] or UUID(int=0),
                            user_id=row["user_id"] or UUID(int=0),
                        )
                    ),
                )
            )

        avg_rating = (
            overall_rating / total_review_count if total_review_count > 0 else 0.0
        )

        return RecipeReviewRead(
            total_review_count=total_review_count,
            review_count_5=review_count_5,
            review_count_4=review_count_4,
            review_count_3=review_count_3,
            review_count_2=review_count_2,
            review_count_1=review_count_1,
            avg_rating=avg_rating,
            review_details=reviews,
        )

    async def create_review(self, review: ReviewCreate, user_id: UUID, username: str):
        print(
            "-------------------------------- Entering RecipeReviewsService.create_review"
        )
        return await self._create(
            RecipeReviews(
                recipe_id=review.recipe_id,
                ratings=review.ratings,
                comment=review.comment,
                user_id=user_id,
                created_by=username,
            )
        )

    async def update_review(self, review: ReviewUpdate, user_id: UUID, username: str):
        print(
            "-------------------------------- Entering RecipeReviewsService.update_review"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            model.recipe_id == review.recipe_id, model.user_id == user_id
        )

        result = await self.session.execute(query)
        review_data = result.scalar_one_or_none()

        if review_data is None:
            return await self.create_review(
                review=ReviewCreate(
                    comment=review.comment or "",
                    ratings=review.ratings or 0,
                    recipe_id=review.recipe_id or UUID(int=0),
                ),
                user_id=user_id,
                username=username,
            )

        review_data.comment = (
            review.comment if review.comment is not None else review_data.comment
        )
        review_data.ratings = (
            review.ratings if review.ratings is not None else review_data.ratings
        )

        return await self._update(RecipeReviews(**review_data.dict()))

    async def delete_review(self, recipe_review_id: UUID):
        print(
            "-------------------------------- Entering RecipeReviewsService.delete_review"
        )
        review_data = await self.get_review_by_recipe_id(recipe_review_id)

        if review_data is None:
            return None

        return await self._delete(RecipeReviews(**review_data.dict()))
