from app.core.database import Base
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор"
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Название проекта"
    )
    workspace_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID рабочего пространства",
    )
    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя, создавшего проект",
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
    workspace: Mapped["Workspace"] = relationship(
        "Workspace", back_populates="projects", lazy="selectin"
    )
    creator: Mapped["User"] = relationship(
        "User", back_populates="created_projects", lazy="selectin"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="project", lazy="selectin"
    )
    users: Mapped[List["ProjectUser"]] = relationship(
        "ProjectUser", back_populates="project", lazy="selectin"
    )
