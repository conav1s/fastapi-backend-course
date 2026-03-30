from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from simple_backend.src.task_tracker.domain.errors import TaskNotFoundError


def register_storage_handlers(app: FastAPI) -> None:
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)

async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "message": exc.message,
            "context": {
                "task_id": exc.task_id
            }
        }
    )