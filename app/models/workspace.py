from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название рабочего пространства")
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID пользователя, создавшего пространство"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего обновления"
    )

    # Связь с создателем (User)
    creator: Mapped["User"] = relationship(
    "User", back_populates="created_workspaces", lazy="selectin"
    )

    # Связь с WorkspaceUser
    users: Mapped[list["WorkspaceUser"]] = relationship(
        "WorkspaceUser", back_populates="workspace", lazy="selectin"
    )

    # Связь с проектами
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="workspace", lazy="selectin"
    )
