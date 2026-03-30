from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    IN_PROGRESS = "in progress"
    CLOSED = "closed"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus

    def copy(self):
        return Task(id=self.id, title=self.title, status=self.status)