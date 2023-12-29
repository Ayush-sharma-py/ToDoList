from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
class Task(BaseModel):
    title: str
    description: str = None

tasks_db = []
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    name: str
    done: bool = False

tasks = []

@app.get("/api/tasks", response_model=List[Task])
async def read_tasks():
    return tasks

@app.post("/api/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task
    return task
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the ToDo List App"}

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks_db.pop(task_id)
    return deleted_task
