from fastapi import HTTPException

class TaskNotFoundErr(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=404,
                         detail=f"Task with id {task_id} not found")

class UserNotFoundErr(HTTPException):
    def __init__(self, username: str):
        super().__init__(status_code=404,
                         detail=f'User with name {username} not found')

class UserAlreadyExistsErr(HTTPException):
    def __init__(self, username: str):
        super().__init__(status_code=403,
                         detail=f'User with name {username} already exists')
