from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, TIMESTAMP
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Уникальный идентификатор")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Имя пользователя")
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, comment="Уникальная электронная почта")
    password: Mapped[str] = mapped_column(Text, nullable=False, comment="Зашифрованный пароль")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, nullable=False, comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="Дата последнего обновления"
    )

    # Связь с Workspace через промежуточную таблицу WorkspaceUser
    workspaces: Mapped[list["WorkspaceUser"]] = relationship(
        "WorkspaceUser", back_populates="user", lazy="selectin"
    )

    # Связь с созданными рабочими пространствами
    created_workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="creator", lazy="selectin"
    )

    # Связь с созданными проектами
    created_projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="creator", lazy="selectin"
    )

    # Связь с созданными задачами
    created_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="creator", lazy="selectin"
    )
