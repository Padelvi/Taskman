from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..utils import get_task, sql_model_to_dict, add_id_to_dict
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get('/')
def index_all_tasks(db: Session = Depends(get_db)):
    query = db.query(models.Task).order_by(models.Task.id)
    return {'tasks': query.all()}

@router.get('/{index}', response_model=schemas.TaskResponse)
def task_detail(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    return sql_model_to_dict(task)

@router.head('/{index}', status_code=204)
def does_task_exist(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    print(task)
    return Response(status_code=204)

@router.post('/', response_model=schemas.TaskResponse, status_code=201)
def create_task(sent_task: schemas.Task, db: Session = Depends(get_db)):
    task_dict = {
        **sent_task.dict(),
        'completed': False
    }
    task = models.Task(**task_dict)
    db.add(task)
    db.commit()
    db.refresh(task)
    return sql_model_to_dict(task)

@router.put('/{index}')
def modify_task(sent_task: schemas.Task, index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    task.title = sent_task.title
    task.description = sent_task.description
    db.commit()
    db.refresh(task)
    return add_id_to_dict(task, index)

@router.patch('/{index}')
def complete_or_uncomplete_task(
        complete: schemas.CompleteTask,index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    task.completed = complete.completed
    db.commit()
    db.refresh(task)
    return add_id_to_dict(task, index)

@router.delete('/{index}', status_code=204)
def delete_task(index: int, db: Session = Depends(get_db)):
    task = get_task(index, db)
    db.delete(task)
    db.commit()
    return Response(status_code=204)
