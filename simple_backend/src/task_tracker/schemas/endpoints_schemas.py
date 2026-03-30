from pydantic import BaseModel, ConfigDict

from simple_backend.src.task_tracker.domain.models import TaskStatus


class TaskCreateModel(BaseModel):
    title: str

class TaskUpdateModel(BaseModel):
    title: str = ""
    status: TaskStatus = TaskStatus.IN_PROGRESS

class TaskResponseModel(BaseModel):
    id: int
    title: str
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)