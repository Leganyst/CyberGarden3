from app.core.database import Base
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class ProjectUser(Base):
    __tablename__ = "project_users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор записи"
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID проекта",
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя",
    )
    access_level: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Уровень доступа (admin, member, viewer, invited)"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
        comment="Дата добавления пользователя",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="Дата последнего изменения записи",
    )

    # Реляции
    project: Mapped["Project"] = relationship(
        "Project", back_populates="users", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="projects", lazy="joined"
    )
