from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schema import Task, TaskCreate, UserCreate
import models, schema, crud
from database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.get('/')
def index():
    return {"message": "Welcome to TodoAPI!"}

@app.put("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, user)

@app.get("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.login(db, email, password)
    if user:
        return user.auth_token

    else:
        return {
                "error": "Incorrect username or password"
                }

@app.get('/tasks')
def get_tasks(token: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    if user:
        return crud.get_tasks(db, user.id)

    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post('/new-task')
def add_task(token: str, task: TaskCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    task.owner_id = user.id
    db_task = crud.create_task(db, task)
    return db_task

@app.put('/edit-task/{task_id}')
def edit_task(task_id: int, token: str, task: Task, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    return crud.edit_task(db, task, task_id, user.id)

@app.delete('/delete/{task_id}')
def delete(task_id: int, token: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)

    return crud.delete_task(db, task_id, user.id)

