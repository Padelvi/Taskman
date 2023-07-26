from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str = ''

class TaskResponse(Task):
    id: int
    completed: bool

class CompleteTask(BaseModel):
    completed: bool

class User(BaseModel):
    name: str
    password: str
