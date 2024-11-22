from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TaskBase(BaseModel):
    """
    Базовая схема задачи.
    """
    name: str = Field(..., max_length=150, description="Название задачи")


class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи.
    """
    project_id: int = Field(..., description="ID проекта, к которому относится задача")
    created_by: int = Field(..., description="ID пользователя, создавшего задачу")


class TaskUpdate(BaseModel):
    """
    Схема для обновления данных задачи.
    """
    name: Optional[str] = Field(None, max_length=150, description="Новое название задачи")


class TaskResponse(TaskBase):
    """
    Схема для ответа с данными задачи.
    """
    id: int = Field(..., description="Уникальный идентификатор задачи")
    project_id: int = Field(..., description="ID проекта, к которому относится задача")
    created_by: int = Field(..., description="ID пользователя, создавшего задачу")
    created_at: datetime = Field(..., description="Дата создания задачи")
    updated_at: datetime = Field(..., description="Дата последнего обновления задачи")

    class Config:
        from_attributes = True


class TaskWithReminders(TaskResponse):
    """
    Схема для ответа с данными задачи и связанных напоминаний.
    """
    reminders: List[dict] = Field(..., description="Список напоминаний, связанных с задачей")
