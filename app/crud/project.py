from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectWithTasks


async def create_project(db: AsyncSession, project_data: ProjectCreate) -> ProjectResponse:
    """
    Создает новый проект.
    :param db: Сессия базы данных.
    :param project_data: Данные для создания проекта.
    :return: Созданный проект в формате Pydantic модели.
    """
    new_project = Project(
        name=project_data.name,
        workspace_id=project_data.workspace_id,
        created_by=project_data.created_by,
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return ProjectResponse.model_validate(new_project)


async def update_project(
    db: AsyncSession, project_id: int, project_data: ProjectUpdate
) -> Optional[ProjectResponse]:
    """
    Обновляет данные проекта.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :param project_data: Новые данные для обновления проекта.
    :return: Обновленный проект в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        return None

    if project_data.name is not None:
        project.name = project_data.name

    await db.commit()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    """
    Удаляет проект.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        return False

    await db.delete(project)
    await db.commit()
    return True


async def get_project_by_id(
    db: AsyncSession, project_id: int
) -> Optional[ProjectResponse]:
    """
    Извлекает проект по ID.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Проект в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project:
        return ProjectResponse.model_validate(project)
    return None


async def get_project_with_tasks(
    db: AsyncSession, project_id: int
) -> Optional[ProjectWithTasks]:
    """
    Извлекает проект с его задачами.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Проект с задачами в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.tasks))
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if project:
        project_data = ProjectWithTasks.model_validate(project)
        project_data.tasks = [
            {"id": task.id, "name": task.name} for task in project.tasks
        ]
        return project_data
    return None
 