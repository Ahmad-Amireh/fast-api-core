import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# JWT settings
SECRET_KEY = "your-super-secret-key"  # change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------------------
# Password hashing with bcrypt
# ------------------------------
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    # truncate to 72 bytes (bcrypt limitation)
    pw = password[:72].encode("utf-8")
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password[:72].encode("utf-8"),
        hashed.encode("utf-8")
    )

# ------------------------------
# JWT token functions
# ------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
    


def get_current_user(token: str = Depends(oauth2_schema),
                      db: Session = Depends(get_session)):
    from crud import get_user_by_email
    #1- Client sends request
    #2- Token extracted
    #3- Token decoded
    #4- Email extracted
    #5- User fetched
    #6- User returned
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    email = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user