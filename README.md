# To-Do List API

A small CRUD REST API for managing tasks, built with **FastAPI** and **SQLModel** on top of **SQLite**.

Each task has three fields:

| Field   | Type    | Notes                                  |
| ------- | ------- | -------------------------------------- |
| `id`    | int     | Primary key, assigned automatically    |
| `title` | string  | Required, must not be blank            |
| `done`  | boolean | Defaults to `false` on creation        |

---

## Requirements

- Python 3.12
- `fastapi`, `uvicorn`, `sqlmodel`

```bash
pip install fastapi uvicorn sqlmodel
```

## Running the API

Run from the project root (`todo-list-api/`):

```bash
uvicorn app.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`, with interactive docs at:

- Swagger UI — `http://127.0.0.1:8000/docs`
- ReDoc — `http://127.0.0.1:8000/redoc`

---

## Endpoints

All routes are under the `/tasks` prefix.

| Method   | Path          | Description                    | Success | Errors                        |
| -------- | ------------- | ------------------------------ | ------- | ----------------------------- |
| `GET`    | `/tasks/`     | List all tasks                 | 200     | —                             |
| `GET`    | `/tasks/{id}` | Get a single task by id        | 200     | 404 if not found              |
| `POST`   | `/tasks/`     | Create a task                  | 201     | 400 if title is blank         |
| `PUT`    | `/tasks/{id}` | Replace a task's title + done  | 200     | 400 blank title, 404 missing  |
| `DELETE` | `/tasks/{id}` | Delete a task                  | 200     | 404 if not found              |

## Why SQLite?

SQLite is the right fit for a small API like this one:

- **It's a single file.** The whole database is one file on disk (`tasks.db`). There is no server process to run, no port to manage, and no connection string to configure — you can copy, back up, delete, or inspect the database by handling one file.
- **Zero setup.** SQLite ships with Python (`sqlite3` is part of the standard library), so there is nothing to install, no service to start, and no user/password/permissions to create before the first request. Cloning the project and running `uvicorn` is enough — the file and its schema are created for you.
- **It survives restarts.** Unlike an in-memory store (a Python dict, or `sqlite:///:memory:`), the data is written to disk. Stop the server, reboot the machine, come back tomorrow — the tasks are still there. This is the property that makes the API genuinely useful rather than a demo that resets on every reload.

The trade-off is that SQLite is a local, file-based database: it handles one writer at a time and doesn't serve multiple application instances over a network. For a single-process to-do API that's fine. A production deployment with several workers or hosts would move to PostgreSQL — since SQLModel/SQLAlchemy sits in between, that's a change to the connection URL rather than a rewrite of the data layer.

## Where the database file lives

The connection URL is defined in [app/database/database.py](app/database/database.py):

```python
DATABASE_URL = "sqlite:///tasks.db"
```

- The file is named **`tasks.db`** and is **created automatically** the first time the app starts — you never create it by hand. On startup, `create_db_and_tables()` runs `SQLModel.metadata.create_all(engine)`, which creates the file if it's missing and creates the `tasks` table from the `Task` model. If the file already exists, the existing data is left untouched.
- The path is **relative to the directory you launch the app from**, so running `uvicorn app.main:app` from the project root puts `tasks.db` at `todo-list-api/tasks.db`, next to this README. Launching from a different working directory would create a separate, empty `tasks.db` there — so always start the server from the project root.
- **Seeding:** on startup, if the `tasks` table is empty, three starter tasks are inserted ("Learn FastAPI", "Learn SQLModel", "Build CRUD API"). This only happens when the table has no rows, so it won't duplicate or overwrite anything on later runs.
- **Resetting the database:** stop the server, delete `tasks.db`, and start again — a fresh file is created and re-seeded.

---

## Screenshots

## Get All Tasks 

<img width="1437" height="840" alt="Screenshot 2026-08-20 100713" src="https://github.com/user-attachments/assets/e24a220c-5bd6-4d33-8308-639c29730104" />

## Get Task by Id 

<img width="1432" height="768" alt="Screenshot 2026-08-20 101616" src="https://github.com/user-attachments/assets/078995a8-b96f-44a8-9521-5e6054550db9" />

## Get Task - Not Found 

<img width="1430" height="781" alt="Screenshot 2026-08-20 101712" src="https://github.com/user-attachments/assets/b5cb752e-fb88-4ba0-9a44-8785cebe00b4" />

## Add New Task

<img width="892" height="722" alt="Screenshot 2026-08-20 101928" src="https://github.com/user-attachments/assets/7a511f38-1010-4f9c-a644-b0c92b05b849" />

## Add New Task - Title Required 

<img width="900" height="722" alt="Screenshot 2026-08-20 102303" src="https://github.com/user-attachments/assets/716e85bf-f94c-48b6-955c-3528939c9527" />

## Update Task

<img width="902" height="791" alt="Screenshot 2026-08-20 102455" src="https://github.com/user-attachments/assets/eff24710-c30e-4c44-b323-dea52bd72bbc" />

## Update Task - Task Not Found 

<img width="895" height="800" alt="Screenshot 2026-08-20 102659" src="https://github.com/user-attachments/assets/1b45cb1d-67af-4b68-9f14-3782760ce6cb" />


## Update Task - Title Required 

<img width="896" height="798" alt="Screenshot 2026-08-20 102545" src="https://github.com/user-attachments/assets/98ed04dd-43ce-4289-a885-b645fe288361" />

## Delete task 
<img width="905" height="771" alt="Screenshot 2026-08-20 102911" src="https://github.com/user-attachments/assets/e3f05dfe-86d9-4abc-842d-83db921c2aa6" />

## Delete task - Task Not Found

<img width="1441" height="787" alt="Screenshot 2026-08-20 102817" src="https://github.com/user-attachments/assets/3993ed82-df19-4e6d-b570-bf1b049fff5d" />

## Project structure

The code is organised in layers, so each file has one job:

```
app/
├── main.py                       # FastAPI app, startup hook, router registration
├── database/database.py          # engine, table creation + seeding, session dependency
├── models/task.py                # Task model (SQLModel table "tasks")
├── routes/task_route.py          # HTTP layer: paths, status codes, dependencies
├── services/task_service.py      # validation + not-found handling
└── repositories/task_repository.py  # database queries (select/add/commit/delete)
tasks.db                          # SQLite database (created automatically)
```

The request flow is `route → service → repository → database`. Routes stay thin, business rules (blank titles, missing tasks) live in the service, and all SQL-facing code is confined to the repository — so swapping the database out only touches the bottom layer.
