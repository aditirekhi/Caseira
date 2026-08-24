from uuid import UUID

from pydantic import BaseModel


class ReviewBaseClass(BaseModel):
    ratings: int
    comment: str | None
    recipe_id: UUID


class ReviewRead(ReviewBaseClass):
    recipe_review_id: UUID
    user_id: UUID
    username: str
    created_at: str | None
    helpful_review_count: int | None
    helpful_review_given_by_user: bool | None


class ReviewCreate(ReviewBaseClass):
    pass


class ReviewUpdate(BaseModel):
    ratings: int | None
    comment: str | None
    recipe_id: UUID | None


class ReviewDelete(BaseModel):
    recipe_review_id: UUID


class RecipeReviewRead(BaseModel):
    total_review_count: int
    review_count_5: int
    review_count_4: int
    review_count_3: int
    review_count_2: int
    review_count_1: int
    avg_rating: float
    review_details: list[ReviewRead]
