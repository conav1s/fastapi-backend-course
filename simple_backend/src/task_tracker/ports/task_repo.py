from abc import ABC, abstractmethod
from typing import Iterable

from simple_backend.src.task_tracker.domain.models import Task

class TaskRepo(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Task]: ...

    # raises: TaskNotFoundError
    @abstractmethod
    def get_by_id(self, task_id: int) -> Task: ...

    @abstractmethod
    def add(self, task: Task) -> None: ...

    @abstractmethod
    def update(self, task: Task) -> None: ...

    # raises: TaskNotFoundError
    @abstractmethod
    def delete(self, task_id: int) -> Task: ...

    def _update_task_fields(self, stored_task: Task, new_task: Task) -> None:
        stored_task.title = new_task.title
        stored_task.status = new_task.status
