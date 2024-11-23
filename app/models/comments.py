from app.core.database import Base
from sqlalchemy import Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Уникальный идентификатор комментария",
    )
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID связанной задачи",
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID автора комментария",
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Текст комментария"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
        comment="Дата создания комментария",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="Дата последнего обновления комментария",
    )

    # Реляции
    task: Mapped["Task"] = relationship("Task", back_populates="comments", lazy="selectin")
    user: Mapped["User"] = relationship("User", back_populates="comments", lazy="selectin")
