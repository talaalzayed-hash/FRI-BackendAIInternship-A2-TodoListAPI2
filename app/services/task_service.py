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

    def create_task(self, title: str):
        if not title or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"message": "Title is required"}
            )
        return self.repository.create(title.strip())

    def update_task(self, task_id: int, title: str, done: bool):
        if not title or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"message": "Title is required"}
            )
        task = self.repository.update(
            task_id,
            title.strip(),
            done
        )
        if task is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Task not found"}
            )
        return task

    def delete_task(self, task_id: int):
        task = self.repository.delete(task_id)
        if task is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Task not found"}
            )
        return task