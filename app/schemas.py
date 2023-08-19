from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str = ''

class TaskResponse(Task):
    id: int
    completed: bool

class CompleteTask(BaseModel):
    completed: bool

class UserLogin(BaseModel):
    name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
