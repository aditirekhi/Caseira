from pydantic import BaseModel


class TipsClass(BaseModel):
    title: str
    description: str
