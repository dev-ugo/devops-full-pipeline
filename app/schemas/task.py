from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """What the client sends to create a task."""
    title: str = Field(..., min_length=1, max_length=255, example="Learn Terraform")
    description: str | None = Field(None, max_length=1000)


class TaskUpdate(BaseModel):
    """All fields are optional - we only update what is provided."""
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None


class TaskResponse(BaseModel):
    """What the API returns for a task."""
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True  # allows reading from a SQLAlchemy object
