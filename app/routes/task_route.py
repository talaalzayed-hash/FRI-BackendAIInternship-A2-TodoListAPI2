from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.database import get_session
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/")
def get_tasks(session: Session = Depends(get_session)):
    repository = TaskRepository(session)
    service = TaskService(repository)

    return service.get_all_tasks()