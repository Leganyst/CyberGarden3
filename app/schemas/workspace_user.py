from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WorkspaceUserBase(BaseModel):
    """
    Базовая схема связи пользователя и рабочего пространства.
    """
    workspace_id: int = Field(..., description="ID рабочего пространства")
    user_id: int = Field(..., description="ID пользователя")
    access_level: str = Field(..., max_length=50, description="Уровень доступа (admin, member, viewer)")


class WorkspaceUserCreate(WorkspaceUserBase):
    """
    Схема для добавления пользователя в рабочее пространство.
    """
    pass


class WorkspaceUserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя в рабочем пространстве.
    """
    access_level: Optional[str] = Field(None, max_length=50, description="Новый уровень доступа (admin, member, viewer)")


class WorkspaceUserResponse(WorkspaceUserBase):
    """
    Схема для ответа с данными о связи пользователя и рабочего пространства.
    """
    id: int = Field(..., description="Уникальный идентификатор записи")
    created_at: datetime = Field(..., description="Дата добавления пользователя")
    updated_at: datetime = Field(..., description="Дата последнего изменения записи")

    class Config:
        from_attributes = True
