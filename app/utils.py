from . import models
from .errors import TaskNotFoundErr, UserNotFoundErr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_task(index, db):
    query = db.query(models.Task).filter_by(id=index)
    task = query.first()
    if task is None:
        raise TaskNotFoundErr(task_id=index)
    return task

def sql_task_to_dict(task: models.Task):
    columns = task.__table__.columns.keys()
    attributes = {c: getattr(task, c) for c in columns}
    return attributes

def add_id_to_task(task, index):
    task_return = {
        'id': index,
        **sql_task_to_dict(task)
    }
    return task_return

def get_user(username, db):
    query = db.query(models.User).filter_by(name=username)
    user = query.first()
    if user is None:
        raise UserNotFoundErr(username=username)
    return user
