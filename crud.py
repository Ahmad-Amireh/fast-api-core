from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, Post, RefreshToken
from schemas import UserCreate, UserUpdate, PostCreate
from security import hash_password
from datetime import datetime, timedelta, timezone
import security


def create_user(session: Session, user_data: UserCreate):
    user = User(name=user_data.name,
                email=user_data.email,
                password = hash_password(user_data.password))
                
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session, skip: int, limit: int):

    stmt = (
        select(User)
        .offset(skip)
        .limit(limit)
    )

    return session.scalars(stmt).all()


def get_user_by_id(
        session: Session,
        user_id: int
):
    return session.get(User, user_id)

def get_user_by_email(session: Session, email: str):
    stmt = select(User).where(User.email == email)
    return session.scalars(stmt).first()

def update_user(session: Session, user_id: int, user_data: UserUpdate):

    user= session.get(User, user_id)

    if not user: 
        return 
    
    if user_data.name: 
        
        user.name= user_data.name
    
    if user_data.email:

        user.email = user_data.email

    if user_data.password:
        user.password = hash_password(user_data.password)

    session.commit()
    session.refresh(user)
    
    return user

def delete_user (session: Session, user_id: int):

    user = session.get(User, user_id)

    if not user:
        return
    
    session.delete(user)
    
    session.commit()

    return True

def create_post_in_db (session: Session, post_data: PostCreate, user_id: int):
    post = Post(title=post_data.title, content=post_data.content, user_id=user_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_posts(session:Session) -> list[Post]:
    stmt = select(Post)
    return session.scalars(stmt).all()

def get_posts_by_user(
    session: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> list[Post]:

    stmt = (
        select(Post)
        .where(Post.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )

    return session.scalars(stmt).all()




def create_refresh_token(session, user_id):

    token = security.create_refresh_token()

    expire = datetime.now(timezone.utc) + timedelta(
        days=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expire_at=expire
    )

    session.add(db_token)
    session.commit()
    session.refresh(db_token)

    return db_token

def get_refresh_token(session, token):

    stmt = select(RefreshToken).where(RefreshToken.token == token)
    return session.scalars(stmt).first()

def delete_refresh_token(session, token):

    db_token = get_refresh_token(session, token)

    if db_token:

        session.delete(db_token)
        session.commit()