from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP, desc
from datetime import datetime

from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP, Boolean, Date
from datetime import datetime, date


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор")
    name: Mapped[str] = mapped_column(String(150), nullable=False, comment="Название задачи")
    description: Mapped[str] = mapped_column(String(500), nullable=True, comment="Описание задачи")
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False, comment="Статус задачи (Открыто / В работе / Проверка / Готово)")
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="ID проекта"
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID пользователя, создавшего задачу"
    )
    assigned_to: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="ID пользователя, которому назначена задача"
    )
    due_date: Mapped[date] = mapped_column(Date, nullable=True, comment="Срок выполнения задачи")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="Флаг выполнения задачи")
    priority: Mapped[str] = mapped_column(
        String(50), default=None, nullable=True, comment="Приоритет задачи (None, low, normal, high)"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего обновления"
    )

    project: Mapped["Project"] = relationship("Project", back_populates="tasks", lazy="selectin")
    # Связи
    creator: Mapped["User"] = relationship(
        "User",
        back_populates="created_tasks",
        lazy="joined",
        foreign_keys="[Task.created_by]",  # Явно указываем внешний ключ
    )


    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="task", lazy="selectin"
    )    

    reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="task", lazy="selectin")
    assigned: Mapped["User"] = relationship("User", foreign_keys=[assigned_to], lazy="selectin")
