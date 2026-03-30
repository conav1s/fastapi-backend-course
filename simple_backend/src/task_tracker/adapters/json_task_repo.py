from pathlib import Path

from simple_backend.src.task_tracker.domain.models import Task
from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError
from simple_backend.src.task_tracker.ports.task_repo import TaskRepo
from simple_backend.src.task_tracker.schemas.infrastructure_schemas import StorageModel


class JsonTaskRepo(TaskRepo):
    def __init__(self, file_path: str = "repo.json") -> None:
        self._file_path = Path(file_path)
        self._ensure_file_exist()
        
    def get_all(self) -> list[Task]:
        storage = self._get_data()

        return storage.tasks
    
    def get_by_id(self, task_id: int) -> Task:
        storage = self._get_data()

        return self._find_by_id(storage, task_id)
    
    def add(self, task: Task) -> None:
        storage = self._get_data()

        storage.last_id += 1
        task.id = storage.last_id

        storage.tasks.append(task)

        self._save_data(storage)

    def update(self, task: Task) -> None:
        storage = self._get_data()

        stored_task = self._find_by_id(storage, task.id)
        self._update_task_fields(stored_task, task)
        self._save_data(storage)

    def delete(self, task_id: int) -> Task:
        storage = self._get_data()

        task = self._find_by_id(storage, task_id)
        out_task = task.copy()
        storage.tasks.remove(task)

        self._save_data(storage)

        return out_task

    def _ensure_file_exist(self) -> None:
        if not self._file_path.exists():
            self._file_path.write_text(
                data=StorageModel(last_id=-1, tasks=[]).model_dump_json(indent=2),
                encoding="utf-8"
            )

    def _get_data(self) -> StorageModel:
        data = self._file_path.read_text(encoding="utf-8")

        return StorageModel.model_validate_json(json_data=data)
    
    def _save_data(self, changed_storage: StorageModel) -> None:
        self._file_path.write_text(
            data=changed_storage.model_dump_json(indent=2, ensure_ascii=False)
        )

    def _find_by_id(self, storage: StorageModel, task_id: int) -> Task:
        for task in storage.tasks:
            if task.id == task_id:
                return task
            
        raise TaskNotFoundError(task_id)
