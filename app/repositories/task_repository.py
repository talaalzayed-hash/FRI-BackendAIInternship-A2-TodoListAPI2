from sqlmodel import Session, select

from app.models.task import Task

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_all(self):
        statement = select(Task)
        return self.session.exec(statement).all()

    def get_by_id(self, task_id: int):
        statement = select(Task).where(Task.id == task_id)
        return self.session.exec(statement).first()