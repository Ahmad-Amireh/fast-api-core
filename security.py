import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt

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