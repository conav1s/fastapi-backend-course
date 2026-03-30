from fastapi import FastAPI

from simple_backend.src.task_tracker.routers.task_storage_router import task_storage_router
from simple_backend.src.task_tracker.register_handlers import register_storage_handlers

app = FastAPI()
app.include_router(task_storage_router)
register_storage_handlers(app)
