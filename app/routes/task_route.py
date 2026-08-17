from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_session
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
def get_tasks(session: Session = Depends(get_session)):
    service = TaskService(session)
    return service.get_all_tasks()

@router.get("/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    service = TaskService(session)
    return service.get_task_by_id(task_id)