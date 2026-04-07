from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """What the client sends to create a task."""
    title: str = Field(..., min_length=1, max_length=255, example="Learn Terraform")
    description: Optional[str] = Field(None, max_length=1000)


class TaskUpdate(BaseModel):
    """All fields are optional - we only update what is provided."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """What the API returns for a task."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # allows reading from a SQLAlchemy object