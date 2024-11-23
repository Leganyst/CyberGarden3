from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List
from app.models.task import Task
from app.models.project import Project
from app.models.workspace import Workspace
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithReminders
from app.schemas.reminder import ReminderResponse
from app.models.reminder import Reminder
from datetime import date, datetime
from fastapi import HTTPException, status


async def create_task(db: AsyncSession, task_data: TaskCreate, current_user_id: int) -> TaskResponse:
    """
    Создает новую задачу с опциональным напоминанием и поддержкой вложенных задач.
    :param db: Сессия базы данных.
    :param task_data: Данные для создания задачи.
    :param current_user_id: ID текущего пользователя.
    :return: Созданная задача в формате Pydantic модели.
    """
    # Проверяем, если указан parent_task_id, то родительская задача должна существовать
    if task_data.parent_task_id:
        parent_task = await db.get(Task, task_data.parent_task_id)
        if not parent_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Родительская задача не найдена."
            )

    # Создание задачи
    new_task = Task(
        name=task_data.name,
        project_id=task_data.project_id,
        created_by=current_user_id,
        assigned_to=task_data.assigned_to if task_data.assigned_to != 0 else None,
        due_date=task_data.due_date,
        priority=task_data.priority,
        description=task_data.description,
        status=task_data.status,
        parent_task_id=task_data.parent_task_id
    )
    db.add(new_task)
    await db.flush()  # Генерируем ID задачи без фиксации транзакции

    # Создание напоминания, если указано время
    if task_data.reminder_time:
        reminder = Reminder(
            task_id=new_task.id,
            reminder_time=task_data.reminder_time,
        )
        db.add(reminder)

    # Фиксируем изменения
    await db.commit()

    # Подгружаем данные задачи вместе с напоминаниями, родительской задачей и подзадачами
    await db.refresh(new_task)

    # Преобразуем данные в формат Pydantic
    task_response = TaskResponse.model_validate(new_task)

    return task_response


async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskUpdate
) -> Optional[TaskResponse]:
    """
    Обновляет данные задачи, включая обновление вложенности.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :param task_data: Новые данные для обновления задачи.
    :return: Обновленная задача в формате Pydantic модели или None, если не найдена.
    """
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена."
        )

    if task_data.name is not None:
        task.name = task_data.name
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed
    if task_data.assigned_to is not None:
        task.assigned_to = task_data.assigned_to if task_data.assigned_to != 0 else None
    if task_data.parent_task_id is not None:
        # Проверяем, если указан parent_task_id, то родительская задача должна существовать
        if task_data.parent_task_id:
            parent_task = await db.get(Task, task_data.parent_task_id)
            if not parent_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Родительская задача не найдена."
                )
        task.parent_task_id = task_data.parent_task_id

    # Фиксируем изменения
    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Удаляет задачу вместе с ее подзадачами (если заданы каскадные удаления).
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: True, если удаление успешно, иначе False.
    """
    task = await db.get(Task, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[TaskResponse]:
    """
    Извлекает задачу по ID вместе с родительской задачей и подзадачами.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(
        select(Task)
        .options(
            selectinload(Task.parent_task).load_only("id", "name", "status", "priority"),
            selectinload(Task.subtasks).load_only("id", "name", "status", "priority")
        )
        .where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    if task:
        return TaskResponse.model_validate(task)
    return None


async def get_task_with_reminders(
    db: AsyncSession, task_id: int
) -> Optional[TaskWithReminders]:
    """
    Извлекает задачу с ее напоминаниями, родительской задачей и подзадачами.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача с напоминаниями в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(
        select(Task)
        .options(
            selectinload(Task.reminders),
            selectinload(Task.parent_task).load_only("id", "name", "status", "priority"),
            selectinload(Task.subtasks).load_only("id", "name", "status", "priority")
        )
        .where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    if task:
        return TaskWithReminders.model_validate(task)
    return None


async def get_tasks_for_project(
    db: AsyncSession, project_id: int
) -> List[TaskResponse]:
    """
    Извлекает все задачи для проекта вместе с вложенностью.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Список задач в формате Pydantic моделей.
    """
    result = await db.execute(
        select(Task)
        .options(
            selectinload(Task.parent_task).load_only("id", "name", "status", "priority"),
            selectinload(Task.subtasks).load_only("id", "name", "status", "priority")
        )
        .where(Task.project_id == project_id)
    )
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]


async def get_user_tasks_by_date(
    db: AsyncSession, user_id: int, target_date: date
) -> List[dict]:
    """
    Извлекает все задачи пользователя на указанную дату с указанием проектов и рабочих пространств.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :param target_date: Дата, для которой извлекаются задачи.
    :return: Список задач в виде словарей.
    """
    # Запрос задач пользователя на указанную дату
    tasks_query = (
        select(
            Task.id,
            Task.name,
            Task.due_date,
            Task.is_completed,
            Task.created_at,
            Task.updated_at,
            Project.name.label("project_name"),
            Workspace.name.label("workspace_name"),
        )
        .join(Project, Task.project_id == Project.id)
        .join(Workspace, Project.workspace_id == Workspace.id)
        .where(
            Task.assigned_to == user_id,  # Условие: задачи, назначенные пользователю
            Task.due_date == target_date,  # Условие: задачи на указанную дату
        )
        .order_by(Task.due_date, Task.id)  # Сортировка
    )

    # Выполнение запроса
    result = await db.execute(tasks_query)
    rows = result.fetchall()

    # Преобразование данных в список словарей
    tasks = [
        {
            "id": row.id,
            "name": row.name,
            "project": row.project_name,
            "workspace": row.workspace_name,
            "due_date": row.due_date.isoformat() if row.due_date else None,
            "is_completed": row.is_completed,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
        }
        for row in rows
    ]

    return tasks
