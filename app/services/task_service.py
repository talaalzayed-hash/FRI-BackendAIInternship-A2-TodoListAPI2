from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.repositories.task_repository import TaskRepository

class TaskService:

    def __init__(self, session: Session):
        self.repository = TaskRepository(session)

    def get_all_tasks(self):
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        if task is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Task not found"}
            )
        return task