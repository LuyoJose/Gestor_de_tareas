from fastapi import FastAPI, HTTPException
from typing import List
from app import Task

app = FastAPI()

# Base de datos en memoria (lista)
tasks = []

# Ruta para obtener todas las tareas
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Ruta para obtener una tarea por ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Ruta para crear una nueva tarea
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# Ruta para actualizar una tarea existente
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# Ruta para eliminar una tarea por ID
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)