from app.models.task import Task
from app.repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all_tasks(self) -> list[Task]:
        return self.repository.get_all_tasks()