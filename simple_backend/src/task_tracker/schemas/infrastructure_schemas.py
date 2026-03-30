from pydantic import BaseModel

from simple_backend.src.task_tracker.domain.models import Task


class StorageModel(BaseModel):
    last_id: int
    tasks: list[Task]