from fastapi import FastAPI, HTTPException, Query

from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError
from simple_backend.src.task_tracker.services.task_service import TaskService
from simple_backend.src.task_tracker.adapters.dict_task_repo import DictTaskRepo
from simple_backend.src.task_tracker.adapters.json_task_repo import JsonTaskRepo
from simple_backend.src.task_tracker.schemas.task_schemas import TaskCreateModel, TaskUpdateModel

app = FastAPI()

task_service = TaskService(repo=JsonTaskRepo())
# task_service = TaskService(repo=DictTaskRepo())

@app.get("/tasks")
def get_tasks():
    return task_service.get_all()

@app.post("/tasks")
def create_task(task_create_input: TaskCreateModel = Query()):
    task = task_service.create(title=task_create_input.title)
    return f"Successful created task '{task.title}'"

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update_input: TaskUpdateModel = Query()):
    try:
        task = task_service.update(
            task_id=task_id,
            title=task_update_input.title,
            status=task_update_input.status
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id '{task_id}' doesn't exist"
        )
    
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        task = task_service.delete(task_id=task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id '{task_id}' doesn't exist"
        )
    
    return f"Task '{task.title}' deleted"
