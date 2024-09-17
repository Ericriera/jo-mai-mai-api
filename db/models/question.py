from pydantic import BaseModel
from typing import Optional


class Question(BaseModel):
    id: Optional[str] = None
    question: dict
    categories: list
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
