from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Suggestion(BaseModel):
    id: Optional[str] = None
    suggestion: str
    category: str
    created_at: Optional[datetime] = None
