from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False


tasks_db = []


@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task_dict = task.dict()
    task_dict["id"] = len(tasks_db) + 1
    tasks_db.append(task_dict)
    return task_dict


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    index = task_id - 1
    if index < 0 or index >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[index] = task.dict()
    tasks_db[index]["id"] = task_id
    return tasks_db[index]


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    index = task_id - 1
    if index < 0 or index >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[index]
    return {"message": "Task deleted successfully"}

if __name__ == '__main__':
    import requests

    url = "http://127.0.0.1:8000/tasks"

    tasks_data = [
        {"title": "Complete project report", "description": "Write a detailed report on the completed project",
         "status": False},
        {"title": "Schedule meeting with client",
         "description": "Arrange a meeting with the client to discuss project updates", "status": True},
        {"title": "Review feedback from team members",
         "description": "Read and address any feedback provided by team members on the project", "status": False},
        {"title": "Prepare presentation for stakeholders",
         "description": "Create a presentation to update stakeholders on project progress", "status": True},
        {"title": "Research new technology trends",
         "description": "Gather information on emerging technology trends relevant to the project", "status": False}
    ]

    for task_data in tasks_data:
        response = requests.post(url, json=task_data)
        if response.status_code == 200:
            print(f"Задача '{task_data['title']}' успешно добавлена")
        else:
            print(f"Ошибка при добавлении задачи '{task_data['title']}': {response.text}")

