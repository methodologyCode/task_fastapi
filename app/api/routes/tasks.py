from typing import List, Set

from fastapi import (APIRouter, Depends, HTTPException,
                     WebSocket, WebSocketDisconnect)

from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from auth.security import get_user_by_token
from ..Service.task import TaskService
from ..Service.user import UserService

router = APIRouter()

active_connections: Set[WebSocket] = set()


@router.websocket("/ws/tasks/{client_id}")
async def websocket_endpoint(client_id: int, websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"Client with {client_id} wrote {message}!")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, username: str = Depends(get_user_by_token)):
    user = await UserService.find_one_or_none(username=username)
    task_db = await TaskService.add(title=task.title, description=task.description,
                                    completed=task.completed, owner_id=user.id)

    for connection in active_connections:
        await connection.send_text(f"New task created: {task_db.title}")

    return task_db 


@router.get("/tasks/", response_model=List[TaskResponse])
async def read_all_tasks():
    tasks = await TaskService.find_all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int):
    task = await TaskService.find_one_or_none(id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    db_task = await TaskService.update(task_id, title=task_update.title,
                                       description=task_update.description,
                                       completed=task_update.completed)

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    

    for connection in active_connections:
        await connection.send_text(f"Task {db_task.id} updated")

    return db_task


@router.delete("/tasks/{task_id}", response_model=TaskResponse)
async def delete_task(task_id: int):
    task = await TaskService.delete(id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for connection in active_connections:
        await connection.send_text(f"Task {task.id} deleted")

    return task