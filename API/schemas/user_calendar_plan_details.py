from datetime import date, datetime
from uuid import UUID

from pydantic import field_validator

from schemas.base import BaseSchema


class UserCalendarPlanDetails(BaseSchema):
    recipe_id: UUID
    plan_date: date


class UserCalendarPlanDetailsRead(UserCalendarPlanDetails):
    user_calendar_plan_id: UUID
    recipe_name: str
    user_id: UUID


class UserCalendarPlanDetailsCreate(UserCalendarPlanDetails):
    @field_validator("plan_date", mode="before")
    @classmethod
    def normalize_plan_date(cls, value: date | str) -> date | str:
        if isinstance(value, str) and "T" in value:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        return value


class UserCalendarPlanDetailsUpdate(UserCalendarPlanDetails):
    recipe_id: UUID | None = None
    plan_date: date | None = None


class UserCalendarPlanDetailsDelete(BaseSchema):
    user_calendar_plan_details_id: UUID
