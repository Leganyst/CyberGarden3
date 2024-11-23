from app.core.database import Base
from sqlalchemy import String, Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор"
    )
    telegram_id: Mapped[str] = mapped_column(
        Text, nullable=True, comment="ID пользователя в Telegram"
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Имя пользователя"
    )
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, comment="Уникальная электронная почта"
    )
    password: Mapped[str] = mapped_column(
        Text, nullable=True, comment="Зашифрованный пароль"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
        comment="Дата создания записи",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="Дата последнего обновления",
    )

    # Реляции
    created_workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace", back_populates="creator", lazy="selectin"
    )
    created_projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="creator", lazy="selectin"
    )
    projects: Mapped[List["ProjectUser"]] = relationship(
        "ProjectUser", back_populates="user", lazy="noload"
    )
    created_tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="creator",
        lazy="selectin",
        foreign_keys="Task.created_by",
    )
    assigned_tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="assigned_user",
        lazy="selectin",
        foreign_keys="Task.assigned_to",
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="user", lazy="selectin"
    )