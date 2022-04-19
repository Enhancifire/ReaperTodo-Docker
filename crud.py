from fastapi.exceptions import HTTPException
import models, schema
import database
import hasher
from uuid import uuid4

from sqlalchemy.orm import Session

def login(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if hasher.dehash(user.hashed_password, user.salt, password):
        return user

    else:
        return None


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.auth_token == token).first()

def create_user(db: Session, user: schema.UserCreate):
    token = str(uuid4())
    key, salt = hasher.hash(user.password)
    db_user = models.User(
            email = user.email,
            hashed_password = key,
            salt = salt,
            auth_token = token,
            )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_task(db: Session, task: schema.TaskCreate):
    db_task = models.Task(
            title = task.title,
            owner_id = task.owner_id
            )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, owner_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == owner_id)

def get_task(db: Session, owner_id: int, task_id: int):
    task =  db.query(models.Task).filter(models.Task.id == task_id).first()
    if task.owner_id == owner_id:
        return task

    else:
        return None

def edit_task(db: Session, new_task: schema.Task, task_id: int, id:int):
    task = get_task(db, id, task_id)
    if not task:
        raise HTTPException(
                status_code= 400,
                detail= "Unauthorized access"
                )

    task.due = new_task.due
    task.title = new_task.title

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, owner_id: int):
    task = get_task(db, owner_id, task_id)
    db.delete(task)
    db.commit()

    return {
            "message": "Task with id: {task_id} deleted successfully"
            }
