from typing import Iterable

from simple_backend.src.task_tracker.domain.models import Task, TaskStatus
from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError
from simple_backend.src.task_tracker.ports.task_repo import TaskRepo


class TaskService:
    def __init__(self, repo: TaskRepo):
        self._repo = repo

    def get_all(self) -> Iterable[Task]:
        return self._repo.get_all()
    
    def create(self, title: str) -> Task:
        task = Task(id=0, title=title, status=TaskStatus.IN_PROGRESS)
        self._repo.add(task=task)

        return task.copy()
        
    def update(self, task_id: int, title: str, status: TaskStatus) -> Task:
        task = self._repo.get_by_id(task_id=task_id)

        if title:
            task.title = title
        
        task.status = status

        self._repo.update(task)

        return task.copy()
    
    def delete(self, task_id: int) -> Task:
        task = self._repo.delete(task_id=task_id)
        
        return task

