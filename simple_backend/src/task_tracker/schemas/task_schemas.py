from pydantic import BaseModel

from simple_backend.src.task_tracker.domain.models import TaskStatus

class TaskCreateModel(BaseModel):
    title: str

class TaskUpdateModel(BaseModel):
    title: str = ""
    status: TaskStatus = TaskStatus.IN_PROGRESS