from uuid import UUID

from pydantic import BaseModel


class HelpfulReviewBaseClass(BaseModel):
    recipe_review_id: UUID


class HelpfulReviewRead(HelpfulReviewBaseClass):
    helpful_review_id: UUID
    user_id: UUID


class HelpfulReviewCreate(HelpfulReviewBaseClass):
    pass


class HelpfulReviewUpdate(BaseModel):
    recipe_review_id: UUID | None


class HelpfulReviewDelete(BaseModel):
    recipe_review_id: UUID
