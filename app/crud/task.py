from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithReminders
from app.models.reminder import Reminder
from datetime import date
from fastapi import HTTPException, status

async def create_task(db: AsyncSession, task_data: TaskCreate, current_user_id: int) -> TaskResponse:
    """
    Создаёт новую задачу с опциональным напоминанием.
    """
    # Проверяем, если указан parent_task_id, то родительская задача должна существовать
    if task_data.parent_task_id:
        parent_task = await db.get(Task, task_data.parent_task_id)
        if not parent_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Родительская задача не найдена."
            )
    # Устанавливаем parent_task_id в None, если оно равно 0
    if task_data.parent_task_id == 0:
        task_data.parent_task_id = None

    # Устанавливаем assigned_to в None, если оно равно 0
    if task_data.assigned_to == 0:
        task_data.assigned_to = None

    # Создание задачи
    new_task = Task(
        name=task_data.name,
        project_id=task_data.project_id,
        created_by=current_user_id,
        assigned_to=task_data.assigned_to,
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

    # Обновляем объект задачи, чтобы получить свежие данные
    await db.refresh(new_task)

    # Преобразуем данные в формат Pydantic
    task_response = TaskResponse(
        id=new_task.id,
        name=new_task.name,
        due_date=new_task.due_date,
        description=new_task.description,
        status=new_task.status,
        priority=new_task.priority,
        project_id=new_task.project_id,
        created_by=new_task.created_by,
        assigned_to=new_task.assigned_to,
        is_completed=new_task.is_completed,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
        parent_task=new_task.parent_task_id
    )

    return task_response

async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskUpdate
) -> Optional[TaskResponse]:
    """
    Обновляет данные задачи.
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
        if task_data.parent_task_id == 0:
            task_data.parent_task_id = None
        task.parent_task_id = task_data.parent_task_id

    # Фиксируем изменения
    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)

async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[TaskResponse]:
    """
    Извлекает задачу по ID без предзагрузки подзадач.
    """
    task = await db.get(Task, task_id)
    if task:
        return TaskResponse.model_validate(task)
    return None

async def get_task_with_reminders(
    db: AsyncSession, task_id: int
) -> Optional[TaskWithReminders]:
    """
    Извлекает задачу с её напоминаниями.
    """
    task = await db.get(Task, task_id)
    if not task:
        return None

    # Предзагружаем напоминания
    await db.refresh(task, ["reminders"])

    return TaskWithReminders.model_validate(task)

async def get_tasks_for_project(
    db: AsyncSession, project_id: int
) -> List[TaskResponse]:
    """
    Извлекает все задачи для проекта без предзагрузки подзадач.
    """
    result = await db.execute(
        select(Task).where(Task.project_id == project_id)
    )
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]

async def get_user_tasks_by_date(
    db: AsyncSession, user_id: int, target_date: date
) -> List[TaskResponse]:
    """
    Извлекает все задачи пользователя на указанную дату.
    """
    result = await db.execute(
        select(Task)
        .where(
            Task.assigned_to == user_id,
            Task.due_date == target_date,
        )
        .order_by(Task.due_date, Task.id)
    )
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]

async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Удаляет задачу по её ID.
    """
    task = await db.get(Task, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def get_user_assigned_tasks(db: AsyncSession, user_id: int) -> List[TaskResponse]:
    """
    Получает все задачи, назначенные пользователю.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Список задач.
    """
    result = await db.execute(select(Task).where(Task.assigned_to == user_id))
    tasks = result.unique().scalars().all()  # Убираем дубли
    return [TaskResponse.model_validate(task) for task in tasks]



async def get_project_tasks(db: AsyncSession, project_id: int) -> List[TaskResponse]:
    """
    Получает все задачи для указанного проекта.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Список задач.
    """
    result = await db.execute(select(Task).where(Task.project_id == project_id))
    tasks = result.unique().scalars().all()  # Используем unique() перед scalars()
    return [TaskResponse.model_validate(task) for task in tasks]
