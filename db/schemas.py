from pydantic import BaseModel, json
from typing import List


class CardBase(BaseModel):
    title: str
    description: str | None = None
    image_dir: str

class Card(CardBase):
    id: str

    class Config:
        orm_mode = True