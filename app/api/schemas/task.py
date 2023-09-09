from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True