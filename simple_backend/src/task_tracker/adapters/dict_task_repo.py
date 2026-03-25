from typing import Iterable

from simple_backend.src.task_tracker.ports.task_repo import TaskRepo
from simple_backend.src.task_tracker.domain.models import Task
from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError


class DictTaskRepo(TaskRepo):
    def __init__(self):
        self._storage: dict[int, Task] = {}
        self._last_id = -1

    def get_all(self) -> Iterable[Task]:
        return tuple(self._storage.values())
    

    def get_by_id(self, task_id: int) -> Task:
        task = self._storage.get(task_id)

        if task is None:
            raise TaskNotFoundError()
        
        return task
    
    def add(self, task: Task) -> None:
        self._last_id += 1
        task.id = self._last_id
        self._storage[self._last_id] = task

    def update(self, task: Task) -> None:
        stored_task = self.get_by_id(task.id)

        stored_task.title = task.title
        stored_task.status = task.status


    def delete(self, task_id: int) -> Task:
        out_task = self._storage.get(task_id)

        if out_task is None:
            raise TaskNotFoundError()
        
        del self._storage[task_id]

        return out_task
