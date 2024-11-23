from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from app.schemas.reminder import ReminderResponse
from app.models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    """
    Базовая схема задачи.
    """
    name: str = Field(..., max_length=255, description="Название задачи")
    due_date: Optional[date] = Field(None, description="Дата выполнения задачи")
    description: Optional[str] = Field(
        None, max_length=500, description="Описание задачи"
    )
    status: TaskStatus = Field(
        TaskStatus.OPEN, description="Статус задачи"
    )
    priority: TaskPriority = Field(
        TaskPriority.NONE, description="Приоритет задачи"
    )

class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи.
    """
    project_id: int = Field(
        ..., description="ID проекта, к которому относится задача"
    )
    assigned_to: Optional[int] = Field(
        None, description="ID пользователя, которому назначена задача"
    )
    parent_task_id: Optional[int] = Field(
        None, description="ID родительской задачи (для вложенных задач)"
    )
    reminder_time: Optional[datetime] = Field(
        None, description="Время напоминания для задачи (опционально)"
    )

class TaskUpdate(BaseModel):
    """
    Схема для обновления данных задачи.
    """
    name: Optional[str] = Field(
        None, max_length=255, description="Новое название задачи"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Новое описание задачи"
    )
    status: Optional[TaskStatus] = Field(
        None, description="Новый статус задачи"
    )
    due_date: Optional[date] = Field(
        None, description="Новая дата выполнения задачи"
    )
    priority: Optional[TaskPriority] = Field(
        None, description="Новый приоритет задачи"
    )
    is_completed: Optional[bool] = Field(
        None, description="Флаг выполнения задачи"
    )
    assigned_to: Optional[int] = Field(
        None, description="Обновление исполнителя задачи"
    )
    parent_task_id: Optional[int] = Field(
        None, description="ID новой родительской задачи (для изменения вложенности)"
    )

class TaskResponse(TaskBase):
    """
    Схема для ответа с данными задачи.
    """
    id: int = Field(..., description="Уникальный идентификатор задачи")
    project_id: int = Field(
        ..., description="ID проекта, к которому относится задача"
    )
    created_by: int = Field(
        ..., description="ID пользователя, создавшего задачу"
    )
    assigned_to: Optional[int] = Field(
        None, description="ID пользователя, которому назначена задача"
    )
    is_completed: bool = Field(..., description="Флаг выполнения задачи")
    created_at: datetime = Field(..., description="Дата создания задачи")
    updated_at: datetime = Field(..., description="Дата последнего обновления задачи")
    parent_task: Optional[int] = Field(None, description="ID родительской задачи")
    class Config:
        orm_mode = True

class TaskWithReminders(TaskResponse):
    """
    Схема для ответа с данными задачи и связанных напоминаний.
    """
    reminders: List[ReminderResponse] = Field(
        default_factory=list, description="Список напоминаний, связанных с задачей"
    )