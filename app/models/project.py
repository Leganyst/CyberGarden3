from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название проекта")
    workspace_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, comment="ID рабочего пространства"
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID пользователя, создавшего проект"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего обновления"
    )

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="projects", lazy="joined")
    creator: Mapped["User"] = relationship("User", back_populates="created_projects", lazy="joined")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project", lazy="selectin")
