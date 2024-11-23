from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProjectUserBase(BaseModel):
    """
    Базовая схема связи пользователя и проекта.
    """
    project_id: int = Field(..., description="ID проекта")
    user_id: int = Field(..., description="ID пользователя")
    access_level: str = Field(
        ..., max_length=50, description="Уровень доступа (admin, member, viewer)"
    )


class ProjectUserCreate(ProjectUserBase):
    """
    Схема для добавления пользователя в проект.
    """
    pass


class ProjectUserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя в проекте.
    """
    access_level: Optional[str] = Field(
        None, max_length=50, description="Новый уровень доступа (admin, member, viewer)"
    )


class ProjectUserResponse(ProjectUserBase):
    """
    Схема для ответа с данными о связи пользователя и проекта.
    """
    id: int = Field(..., description="Уникальный идентификатор записи")
    created_at: datetime = Field(..., description="Дата добавления пользователя")
    updated_at: datetime = Field(..., description="Дата последнего изменения записи")

    class Config:
        from_attributes = True
