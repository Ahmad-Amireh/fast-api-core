from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import Base, engine, get_session
from typing import List
import security
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
#Base.metadata.create_all(bind=engine) # Remove when using alembic

app = FastAPI(title= "User-Post API")


@app.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user (user: schemas.UserCreate, db: Session= Depends(get_session)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

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

@app.post("/posts/", response_model=schemas.PostResponse, status_code=201)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_session), current_user: models.User = Depends(security.get_current_user)):
    return crud.create_post_in_db(
            db,
            post,
            current_user.id
        )

@app.get("/posts/", response_model=List[schemas.PostResponse])
def read_posts(db: Session = Depends(get_session)):
    return crud.get_posts(db)

@app.get("/users/{user_id}/posts", response_model=List[schemas.PostResponse])
def read_posts_by_user(user_id: int, db: Session = Depends(get_session)):
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(404, "User not found")
    return crud.get_posts_by_user(db, user_id)




@app.post("/login", response_model=schemas.TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    db_user = crud.get_user_by_email(db, form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not security.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = security.create_access_token(
        data={"sub": db_user.email}
    )

    refresh_token = crud.create_refresh_token(
        db,
        db_user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer"
    }

@app.get("/posts/me", response_model=List[schemas.PostResponse])
def read_my_posts(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_session),
    current_user: models.User = Depends(security.get_current_user)
):
    skip = (page - 1) * page_size
    return crud.get_posts_by_user(db, current_user.id, skip=skip, limit=page_size)

@app.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str, db = Depends(get_session)):

    db_token = crud.get_refresh_token(db, refresh_token)
    
    if not db_token:

        raise HTTPException(
            401,
            "Invalid refresh token"
        )

    if db_token.expire_at < datetime.now(timezone.utc):

        raise HTTPException(
            401,
            "Refresh token expired"
        )
    
    user = db_token.user

    access_token = security.create_access_token(
        {"sub": user.email}
    )

    return {

        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_session)
):

    crud.delete_refresh_token(
        db,
        refresh_token
    )

    return {"message": "Logged out"}