from __future__ import annotations
from datetime import datetime
from sqlalchemy.sql import func

from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class RefreshToken (Base):
    
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),nullable=False)
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

