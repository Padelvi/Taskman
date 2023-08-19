from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth
from ..utils import get_user, sql_model_to_dict
from ..errors import UserAlreadyExistsErr, UserNotFoundErr

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post('/create', status_code=201)
def create_user(
        sent_user: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    try:
        user = get_user(sent_user.username, db)
    except UserNotFoundErr:
        user = models.User(name=sent_user.username, password=sent_user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return sql_model_to_dict(user)
    else:
        raise UserAlreadyExistsErr(sent_user.username)

# Login route
@router.post('/login', response_model=schemas.Token, status_code=201)
def login(sent_user: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user(sent_user.name, db)
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# Change password route

# Delete current user route (NOT PRIORITIZED)
# @router.delete('/{index}', status_code=204)
# def delete_task(index: int, db: Session = Depends(get_db)):
#     task = get_task(index, db)
#     db.delete(task)
#     db.commit()
#     return Response(status_code=204)
