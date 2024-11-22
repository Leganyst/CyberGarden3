from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithReminders


async def create_task(db: AsyncSession, task_data: TaskCreate) -> TaskResponse:
    """
    Создает новую задачу.
    :param db: Сессия базы данных.
    :param task_data: Данные для создания задачи.
    :return: Созданная задача в формате Pydantic модели.
    """
    new_task = Task(
        name=task_data.name,
        project_id=task_data.project_id,
        created_by=task_data.created_by,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return TaskResponse.model_validate(new_task)


async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskUpdate
) -> Optional[TaskResponse]:
    """
    Обновляет данные задачи.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :param task_data: Новые данные для обновления задачи.
    :return: Обновленная задача в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        return None

    if task_data.name is not None:
        task.name = task_data.name

    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Удаляет задачу.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[TaskResponse]:
    """
    Извлекает задачу по ID.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        return TaskResponse.model_validate(task)
    return None


async def get_task_with_reminders(
    db: AsyncSession, task_id: int
) -> Optional[TaskWithReminders]:
    """
    Извлекает задачу с ее напоминаниями.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача с напоминаниями в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(
        select(Task).options(selectinload(Task.reminders)).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    if task:
        task_data = TaskWithReminders.model_validate(task)
        task_data.reminders = [
            {"id": reminder.id, "reminder_time": reminder.reminder_time, "is_sent": reminder.is_sent}
            for reminder in task.reminders
        ]
        return task_data
    return None


async def get_tasks_for_project(
    db: AsyncSession, project_id: int
) -> List[TaskResponse]:
    """
    Извлекает все задачи для проекта.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Список задач в формате Pydantic моделей.
    """
    result = await db.execute(select(Task).where(Task.project_id == project_id))
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]
