from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор")
    name: Mapped[str] = mapped_column(String(150), nullable=False, comment="Название задачи")
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="ID проекта"
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID пользователя, создавшего задачу"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего обновления"
    )

    project: Mapped["Project"] = relationship("Project", back_populates="tasks", lazy="joined")
    creator: Mapped["User"] = relationship("User", back_populates="created_tasks", lazy="joined")
    reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="task", lazy="selectin")
