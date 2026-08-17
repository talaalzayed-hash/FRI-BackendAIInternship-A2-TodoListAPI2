from sqlmodel import Session, select

from app.models.task import Task


class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all_tasks(self) -> list[Task]:
        statement = select(Task)
        return list(self.session.exec(statement).all())