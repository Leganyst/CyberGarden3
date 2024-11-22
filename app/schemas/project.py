from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProjectBase(BaseModel):
    """
    Базовая схема проекта.
    """
    name: str = Field(..., max_length=100, description="Название проекта")


class ProjectCreate(ProjectBase):
    """
    Схема для создания нового проекта.
    """
    workspace_id: int = Field(..., description="ID рабочего пространства, к которому привязан проект")
    created_by: int = Field(..., description="ID пользователя, создавшего проект")


class ProjectUpdate(BaseModel):
    """
    Схема для обновления проекта.
    """
    name: Optional[str] = Field(None, max_length=100, description="Новое название проекта")


class ProjectResponse(ProjectBase):
    """
    Схема для ответа с данными проекта.
    """
    id: int = Field(..., description="Уникальный идентификатор проекта")
    workspace_id: int = Field(..., description="ID рабочего пространства, к которому привязан проект")
    created_by: int = Field(..., description="ID пользователя, создавшего проект")
    created_at: datetime = Field(..., description="Дата создания проекта")
    updated_at: datetime = Field(..., description="Дата последнего обновления проекта")

    class Config:
        orm_mode = True


class ProjectWithTasks(ProjectResponse):
    """
    Схема для ответа с данными проекта и связанных задач.
    """
    tasks: List[dict] = Field(..., description="Список задач, связанных с проектом")
