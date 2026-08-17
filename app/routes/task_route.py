from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_session
from app.models.task import Task
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

@router.post("/", status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    service = TaskService(session)
    return service.create_task(task.title)

@router.put("/{task_id}")
def update_task(task_id: int, task: Task, session: Session = Depends(get_session)):
    service = TaskService(session)
    return service.update_task(
        task_id,
        task.title,
        task.done
    )

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    service = TaskService(session)
    return service.delete_task(task_id)