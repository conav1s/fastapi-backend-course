from simple_backend.src.task_tracker.ports.task_repo import TaskRepo
from simple_backend.src.task_tracker.domain.models import Task
from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError
from simple_backend.src.task_tracker.schemas.infrastructure_schemas import StorageModel


class DictTaskRepo(TaskRepo):
    def __init__(self) -> None:
        self._storage = StorageModel(last_id=-1, tasks=[])

    def get_all(self) -> list[Task]:
        return self._storage.tasks.copy()
    
    def get_by_id(self, task_id: int) -> Task:
        return self._get_by_id_ref(task_id).copy()
    
    def add(self, task: Task) -> None:
        self._storage.tasks.append(task)
        self._storage.last_id += 1
        task.id = self._storage.last_id

    def update(self, task: Task) -> None:
        stored_task = self._get_by_id_ref(task.id)
        self._update_task_fields(stored_task, task)

    def delete(self, task_id: int) -> Task:
        stored_task = self._get_by_id_ref(task_id)
        out_task = stored_task.copy()
        self._storage.tasks.remove(stored_task)
        return out_task

    def _get_by_id_ref(self, task_id: int) -> Task:
        for task in self._storage.tasks:
            if task_id == task.id:
                return task
        
        raise TaskNotFoundError(task_id)
