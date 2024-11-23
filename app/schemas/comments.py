from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class CommentBase(BaseModel):
    """
    Базовая схема для комментария.
    """
    content: str = Field(..., max_length=1000, description="Текст комментария")


class CommentCreate(CommentBase):
    """
    Схема для создания нового комментария.
    """
    task_id: int = Field(..., description="ID задачи, к которой добавляется комментарий")


class CommentUpdate(BaseModel):
    """
    Схема для обновления существующего комментария.
    """
    content: str = Field(..., max_length=1000, description="Обновлённый текст комментария")


class CommentResponse(CommentBase):
    """
    Схема для ответа с данными комментария.
    """
    id: int = Field(..., description="Уникальный идентификатор комментария")
    task_id: int = Field(..., description="ID задачи, к которой принадлежит комментарий")
    user_id: int = Field(..., description="ID автора комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")
    updated_at: datetime = Field(..., description="Дата последнего обновления комментария")

    class Config:
        from_attributes = True


class CommentsListResponse(BaseModel):
    """
    Список комментариев, связанных с задачей.
    """
    comments: List[CommentResponse] = Field(..., description="Список комментариев")
