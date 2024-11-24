from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import List, Dict
from app.models.task import Task
from app.models.project import Project
from app.models.project_user import ProjectUser


async def get_user_task_statistics(db: AsyncSession, user_id: int) -> List[Dict[str, any]]:
    """
    Собирает статистику по задачам пользователя.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Список статистики по проектам.
    """
    # Считаем общее количество задач и разбивку по статусам для каждого проекта пользователя
    result = await db.execute(
        select(
            Project.name.label("project_name"),
            func.count(Task.id).label("total_tasks"),
            func.sum(func.case([(Task.status == "OPEN", 1)], else_=0)).label("open_tasks"),
            func.sum(func.case([(Task.status == "IN_PROGRESS", 1)], else_=0)).label("in_progress_tasks"),
            func.sum(func.case([(Task.status == "COMPLETED", 1)], else_=0)).label("completed_tasks"),
        )
        .join(Task, Task.project_id == Project.id)
        .join(ProjectUser, ProjectUser.project_id == Project.id)
        .where(ProjectUser.user_id == user_id)
        .group_by(Project.id)
    )

    # Формируем статистику в виде словаря
    statistics = [
        {
            "project_name": row.project_name,
            "total_tasks": row.total_tasks,
            "open_tasks": row.open_tasks,
            "in_progress_tasks": row.in_progress_tasks,
            "completed_tasks": row.completed_tasks,
        }
        for row in result
    ]

    return statistics
