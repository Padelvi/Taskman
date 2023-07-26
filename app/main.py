from fastapi import FastAPI
from . import models
from .database import engine
from .routers import tasks_router, users_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks_router.router)
app.include_router(users_router.router)
