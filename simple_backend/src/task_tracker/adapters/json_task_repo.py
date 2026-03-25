import json
import bisect
from pathlib import Path

from simple_backend.src.task_tracker.domain.models import Task, TaskStatus
from simple_backend.src.task_tracker.ports.task_repo import TaskRepo
from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError


class JsonTaskRepo(TaskRepo):
    def __init__(self, file_path: str = "repo.json"):
        self._file_path = Path(file_path)
        self._ensure_file_exist()
        
    def get_all(self) -> tuple[Task]:
        storage, _ = self._get_data()
        return tuple(storage)
    
    def get_by_id(self, task_id: int) -> Task:
        storage, _ = self._get_data()
        for task in storage:
            if task.id == task_id:
                return task
        
        raise TaskNotFoundError()

    def add(self, task: Task) -> None:
        storage, last_id = self._get_data()
        last_id += 1
        task.id = last_id

        storage.append(task)
        self._save_data(storage, last_id)

    def update(self, task: Task) -> None:
        storage, last_id = self._get_data()

        for i, stored_task in enumerate(storage):
            if stored_task.id == task.id:
                storage[i] = task
                self._save_data(storage, last_id)
                return

        raise TaskNotFoundError

    def delete(self, task_id: int) -> Task:
        storage, last_id = self._get_data()
        
        for i, task in enumerate(storage):
            if task.id == task_id:
                out_task = task
                del storage[i]
                self._save_data(storage, last_id)
                return out_task
            
        raise TaskNotFoundError()

    
    def _ensure_file_exist(self) -> None:
        if not self._file_path.exists():
            self._file_path.write_text(
                json.dumps({"last_id" : -1, "tasks": []}, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

    def _get_data(self) -> tuple[list[Task], int]:
        data = json.loads(self._file_path.read_text(encoding="utf-8"))

        return [
            Task(obj["id"], obj["title"], TaskStatus(obj["status"]))
            for obj in data["tasks"]
        ], data["last_id"]
    
    def _save_data(self, storage: list[Task], last_id: int) -> None:
        data = {
            "last_id": last_id,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status.value
                }
                for task in storage
            ]
        }

        self._file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

