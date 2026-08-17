from fastapi import FastAPI
from sqlmodel import inspect
from app.database.database import create_db_and_tables, engine
from app.models.task import Task  # important
from app.routes.task_route import router as task_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print(inspect(engine).get_table_names())

app.include_router(task_router)