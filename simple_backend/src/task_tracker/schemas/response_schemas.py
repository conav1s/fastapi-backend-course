from pydantic import BaseModel

from simple_backend.src.task_tracker.domain.models import Task


class GetEndpointResponseModel(BaseModel):
    tasks: list[Task]
