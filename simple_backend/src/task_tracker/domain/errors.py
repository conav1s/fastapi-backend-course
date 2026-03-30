class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.message = f"Task with id '{task_id}' isn't founded"