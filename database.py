from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL= "sqlite:///example.db"

engine = create_engine(DATABASE_URL, echo= False, future=True)

SessionLocal = sessionmaker(
    bind= engine,
    autoflush = False,
    autocommit = False
)

class Base(DeclarativeBase):
    pass 

def get_session():
    session = SessionLocal()
    try: 
        yield session
    finally:
        session.close()

