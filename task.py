# Задание

# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. 
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.

from random import choice
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic_models import Task


tasks: list[Task] = []

for i in range(10):
    tasks.append(Task(id=i, title=f'title_{i}', description=f'description_{i}', status=f'{choice(["not started", "in progress", "done"])}'))


app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/")
async def index ():
    return tasks

@app.get("/tasks/", response_class=HTMLResponse)
async def get_tasks (request: Request):
    return templates.TemplateResponse("index.html", {'request': request, 'tasks': tasks, 'title': 'Tasks'})


@app.get("/tasks/{task_id}")
async def get_task (task_id: int):
    list_tasks = [task for task in tasks if task.id == task_id]
    return list_tasks


@app.post('/tasks/')
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task: Task):
    task_to_update = [task for task in tasks if task.id == task_id]
    task_to_update[0].title = task.title
    task_to_update[0].description = task.description
    task_to_update[0].status = task.status
    return task_to_update