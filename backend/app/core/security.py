# ResearchHub AI - Security Utilities
# Milestone 3: Activity 3.1 - Build authentication endpoints
# Responsible: Abhishek Kumar (TeamLead)

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from backend.app.core.config import settings


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    Abhishek Kumar (TeamLead) - Password security.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its bcrypt hash.
    Abhishek Kumar (TeamLead) - Password verification.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT access token.
    Abhishek Kumar (TeamLead) - JWT token generation.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    Abhishek Kumar (TeamLead) - JWT token validation.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
