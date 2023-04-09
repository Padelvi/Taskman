from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import get_task, sql_task_to_dict, add_id_to_task
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def index_all_tasks(db: Session = Depends(get_db)):
    query = db.query(models.Task).order_by(models.Task.id)
    return {'tasks': query.all()}

@app.get('/{index}', response_model=schemas.TaskResponse)
def task_detail(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    return sql_task_to_dict(task)

@app.head('/{index}', status_code=204)
def does_task_exist(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    return Response(status_code=204)

@app.post('/', response_model=schemas.TaskResponse, status_code=201)
def create_task(sent_task: schemas.Task, db: Session = Depends(get_db)):
    task_dict = {
        **sent_task.dict(),
        'completed': False
    }
    task = models.Task(**task_dict)
    db.add(task)
    db.commit()
    db.refresh(task)
    return sql_task_to_dict(task)

@app.put('/{index}')
def modify_task(sent_task: schemas.Task, index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    task.title = sent_task.title
    task.description = sent_task.description
    db.commit()
    db.refresh(task)
    return add_id_to_task(task, index)

@app.patch('/{index}')
def complete_or_uncomplete_task(complete: schemas.CompleteTask, index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    task.completed = complete.completed
    db.commit()
    db.refresh(task)
    return add_id_to_task(task, index)

@app.delete('/{index}', status_code=204)
def delete_task(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    db.delete(task)
    db.commit()
    return Response(status_code=204)
