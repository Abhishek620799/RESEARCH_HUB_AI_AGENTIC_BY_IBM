# ResearchHub AI - Authentication Router
# Milestone 3: Activity 3.1 - Build authentication endpoints
# Responsible: Abhishek Kumar (TeamLead)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, Token, LoginRequest
from backend.app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with hashed password."""
    # Check if email or username already exists
    existing = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # Create new user with hashed password
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Dependency: Decode JWT token and return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/create_test_user")
def create_test_user(db: Session = Depends(get_db)):
    """Create a test user for easy login."""
    test_user = User(
        email="test@example.com",
        username="test",
        full_name="Test User",
        hashed_password=get_password_hash("password")
    )
    db.add(test_user)
    db.commit()
    return {"message": "Test user created: username=test, password=password"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user
