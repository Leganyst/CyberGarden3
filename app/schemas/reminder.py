from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReminderBase(BaseModel):
    """
    Базовая схема напоминания.
    """
    task_id: int = Field(..., description="ID связанной задачи")
    reminder_time: datetime = Field(..., description="Время, когда должно быть отправлено напоминание")


class ReminderCreate(ReminderBase):
    """
    Схема для создания нового напоминания.
    """
    is_sent: Optional[bool] = Field(False, description="Статус отправки напоминания (по умолчанию: False)")


class ReminderUpdate(BaseModel):
    """
    Схема для обновления данных напоминания.
    """
    reminder_time: Optional[datetime] = Field(None, description="Новое время напоминания")
    is_sent: Optional[bool] = Field(None, description="Обновленный статус отправки напоминания")


class ReminderResponse(ReminderBase):
    """
    Схема для ответа с данными напоминания.
    """
    id: int = Field(..., description="Уникальный идентификатор напоминания")
    is_sent: bool = Field(..., description="Статус отправки напоминания")
    created_at: datetime = Field(..., description="Дата создания напоминания")

    class Config:
        from_attributes = True
