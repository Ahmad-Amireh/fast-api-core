from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from database import Base
from typing import List


class User (Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key= True,
                                    index= True)
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # ✅ Add this
    

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):

        return f"<User id = {self.id} name= {self.name} email= {self.email}>"