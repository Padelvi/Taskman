from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth
from ..utils import get_user
from ..errors import UserAlreadyExistsErr, UserNotFoundErr

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post('/create', response_model=schemas.UserLogin, status_code=201)
def create_user(sent_user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user = get_user(sent_user.name, db)
    except UserNotFoundErr:
        user = models.User(**sent_user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return sent_user
    else:
        raise UserAlreadyExistsErr(sent_user.name)

# Login route
@router.post('/login', response_model=schemas.UserLogin, status_code=201)
def login(sent_user: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user(sent_user.name, db)
    return {"access_token": access_token, "token_type": "bearer"}
# Logout route

# Change password route

# Change username route


# Delete current user route
# @router.delete('/{index}', status_code=204)
# def delete_task(index: int, db: Session = Depends(get_db)):
#     task = get_task(index, db)
#     db.delete(task)
#     db.commit()
#     return Response(status_code=204)
