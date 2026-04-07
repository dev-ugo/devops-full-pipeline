from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Ce que le client envoie pour créer une tâche."""
    title: str = Field(..., min_length=1, max_length=255, example="Apprendre Terraform")
    description: Optional[str] = Field(None, max_length=1000)


class TaskUpdate(BaseModel):
    """Tous les champs sont optionnels - on ne met à jour que ce qu'on envoie."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Ce que l'API renvoie - jamais plus, jamais moins."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # permet de lire depuis un objet SQLAlchemy