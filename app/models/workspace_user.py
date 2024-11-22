from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

class WorkspaceUser(Base):
    __tablename__ = "workspace_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор записи")
    workspace_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, comment="ID рабочего пространства"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID пользователя"
    )
    access_level: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Уровень доступа (admin, member, viewer)"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата добавления пользователя"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего изменения записи"
    )

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="users", lazy="joined")
    user: Mapped["User"] = relationship("User", back_populates="workspaces", lazy="joined")
