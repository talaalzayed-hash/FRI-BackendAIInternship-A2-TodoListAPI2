from sqlmodel import Session, SQLModel, create_engine, select
from app.models.task import Task

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

        if len(tasks) == 0:
            seed_tasks = [
                Task(title="Learn FastAPI", done=False),
                Task(title="Learn SQLModel", done=False),
                Task(title="Build CRUD API", done=False),
            ]

            session.add_all(seed_tasks)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session