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

    def create(self, title: str):
        task = Task(
            title=title,
            done=False
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def update(self, task_id: int, title: str, done: bool):
        task = self.get_by_id(task_id)
        if task is None:
            return None
        task.title = title
        task.done = done
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)
        if task is None:
            return None
        self.session.delete(task)
        self.session.commit()
        return task