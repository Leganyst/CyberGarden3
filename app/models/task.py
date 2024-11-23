from app.core.database import Base
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор"
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название задачи"
    )
    description: Mapped[str] = mapped_column(
        String(500), nullable=True, comment="Описание задачи"
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, comment="ID создателя задачи"
    )
    assigned_to: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, comment="ID исполнителя задачи"
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False, comment="ID проекта"
    )
    parent_task_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True,
        comment="ID родительской задачи",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
        comment="Дата создания задачи",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="Дата последнего обновления задачи",
    )

    # Реляции
    creator: Mapped["User"] = relationship(
        "User", back_populates="created_tasks", foreign_keys=[created_by]
    )
    assigned_user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assigned_to]
    )
    project: Mapped["Project"] = relationship(
        "Project", back_populates="tasks", lazy="selectin"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="task", lazy="selectin"
    )
    reminders: Mapped[List["Reminder"]] = relationship(
        "Reminder", back_populates="task", lazy="joined"
    )

    # Связи для вложенных задач
    parent_task: Mapped[Optional["Task"]] = relationship(
        "Task",
        remote_side="Task.id",
        back_populates="subtasks",
        lazy="selectin",
    )
    subtasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="parent_task",
        lazy="selectin",
    )
