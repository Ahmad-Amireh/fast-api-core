from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import Base, engine, get_session
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title= "User-Post API")


@app.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user (user: schemas.UserCreate, db: Session= Depends(get_session)):
    return crud.create_user(session=db, user_data= user)

@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_session)
):
    skip = (page - 1) * page_size

    return crud.get_users(db, skip, page_size)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_session)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.post("/users/{user_id}/posts", response_model=schemas.PostResponse, status_code=201)
def create_post(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_session)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    return crud.create_post(db, post, user_id)

@app.get("/posts/", response_model=List[schemas.PostResponse])
def read_posts(db: Session = Depends(get_session)):
    return crud.get_posts(db)

@app.get("/users/{user_id}/posts", response_model=List[schemas.PostResponse])
def read_posts_by_user(user_id: int, db: Session = Depends(get_session)):
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(404, "User not found")
    return crud.get_posts_by_user(db, user_id)