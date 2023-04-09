from . import models
from fastapi import HTTPException

class TaskNotFoundErr(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Task with id {task_id} not found")

def get_task(index, db):
    query = db.query(models.Task).filter_by(id=index)
    task = query.first()
    if task is None:
        raise TaskNotFoundErr(task_id=index)
    return task

def sql_task_to_dict(task: models.Task):
    task_dict = task.__dict__
    columns = task.__table__.columns.keys()
    attributes = {c: getattr(task, c) for c in columns}
    return attributes

def add_id_to_task(task, index):
    task_return = {
        'id': index,
        **sql_task_to_dict(task)
    }
    return task_return
