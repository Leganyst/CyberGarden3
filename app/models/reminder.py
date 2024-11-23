from app.core.database import Base
from sqlalchemy import Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор"
    )
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID связанной задачи",
    )
    reminder_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, comment="Время напоминания"
    )
    is_sent: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="Отправлено ли напоминание"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
        comment="Дата создания записи",
    )

    task: Mapped["Task"] = relationship("Task", back_populates="reminders", lazy="joined")
