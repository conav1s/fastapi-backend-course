from fastapi import APIRouter, Query

from simple_backend.src.task_tracker.services.task_service import TaskService
from simple_backend.src.task_tracker.adapters.dict_task_repo import DictTaskRepo
from simple_backend.src.task_tracker.adapters.json_task_repo import JsonTaskRepo
from simple_backend.src.task_tracker.schemas.endpoints_schemas import TaskCreateModel, TaskUpdateModel, TaskResponseModel

task_storage_router = APIRouter(prefix="/tasks")
task_storage_service = TaskService(repo=DictTaskRepo())
# task_storage_service = TaskService(repo=JsonTaskRepo())

@task_storage_router.get("", response_model=list[TaskResponseModel])
def get_tasks():
    return task_storage_service.get_all()

@task_storage_router.post("", response_model=TaskCreateModel)
def create_task(task_create_input: TaskCreateModel = Query()):
    task = task_storage_service.create(title=task_create_input.title)

    return TaskResponseModel.model_validate(task)

@task_storage_router.put("/{task_id}", response_model=TaskResponseModel)
def update_task(task_id: int, task_update_input: TaskUpdateModel = Query()):
    task = task_storage_service.update(
        task_id=task_id,
        title=task_update_input.title,
        status=task_update_input.status
    )

    return TaskResponseModel.model_validate(task)

@task_storage_router.delete("/{task_id}", response_model=TaskResponseModel)
def delete_task(task_id: int):
    task = task_storage_service.delete(task_id=task_id)

    return TaskResponseModel.model_validate(task)

