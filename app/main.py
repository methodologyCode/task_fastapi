from fastapi import FastAPI, Depends

from api.routes import users, tasks
from api.middleware.middleware import logging_middleware
from auth.security import get_user_by_token

app = FastAPI()
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"], dependencies=[Depends(get_user_by_token)])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.middleware("http")(logging_middleware)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Real-Time Task Manager API"}