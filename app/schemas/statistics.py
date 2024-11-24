from pydantic import BaseModel


class TaskStatistics(BaseModel):
    project_name: str
    total_tasks: int
    open_tasks: int
    in_progress_tasks: int
    completed_tasks: int