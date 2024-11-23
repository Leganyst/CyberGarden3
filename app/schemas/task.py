from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


class TaskBase(BaseModel):
    """
    Базовая схема задачи.
    """
    name: str = Field(..., max_length=150, description="Название задачи")
    due_date: Optional[date] = Field(None, description="Дата выполнения задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    status: Optional[str] = Field(None, description="Статус задачи (Открыто / В работе / Проверка / Готово)")
    priority: Optional[str] = Field(None, description="Приоритет задачи (None, low, normal, high)")


class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи.
    """
    project_id: int = Field(..., description="ID проекта, к которому относится задача")
    assigned_to: Optional[int] = Field(None, description="ID пользователя, которому назначена задача")
    reminder_time: Optional[datetime] = Field(None, description="Время напоминания для задачи (опционально)")
    created_by: int | None = None



class TaskUpdate(BaseModel):
    """
    Схема для обновления данных задачи.
    """
    name: Optional[str] = Field(None, max_length=150, description="Новое название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Новое описание задачи")
    status: Optional[str] = Field(None, description="Новый статус задачи (Открыто / В работе / Проверка / Готово)")
    due_date: Optional[date] = Field(None, description="Новая дата выполнения задачи")
    priority: Optional[str] = Field(None, description="Новый приоритет задачи (None, low, normal, high)")
    is_completed: Optional[bool] = Field(None, description="Флаг выполнения задачи")
    assigned_to: Optional[int] = Field(None, description="Обновление исполнителя задачи")


class TaskResponse(TaskBase):
    """
    Схема для ответа с данными задачи.
    """
    id: int = Field(..., description="Уникальный идентификатор задачи")
    project_id: int = Field(..., description="ID проекта, к которому относится задача")
    created_by: int = Field(..., description="ID пользователя, создавшего задачу")
    assigned_to: Optional[int] = Field(None, description="ID пользователя, которому назначена задача")
    is_completed: bool = Field(..., description="Флаг выполнения задачи")
    created_at: datetime = Field(..., description="Дата создания задачи")
    updated_at: datetime = Field(..., description="Дата последнего обновления задачи")

    class Config:
        from_attributes = True


class TaskWithReminders(TaskResponse):
    """
    Схема для ответа с данными задачи и связанных напоминаний.
    """
    reminders: List[dict] = Field(..., description="Список напоминаний, связанных с задачей")
