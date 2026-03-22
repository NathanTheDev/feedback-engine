from datetime import datetime

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    tags: list[str]
