import os
import subprocess

# ResearchHub AI - Project Setup Script
# Creates the complete project structure

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, 'w') as f:
        f.write(content)
    print(f'Created: {path}')

# Create directories
dirs = [
    'backend/app/routers',
    'backend/app/models',
    'backend/app/schemas',
    'backend/app/services',
    'backend/app/core',
    'frontend/src/components',
    'frontend/src/pages',
    'frontend/src/context',
    'frontend/src/services',
    'frontend/src/types',
    'frontend/public',
]
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f'Created dir: {d}')

print('Directories created!')

# ============ BACKEND FILES ============

# requirements.txt - Milestone 1: Activity 1.1 (Chetan Galphat)
write_file('backend/requirements.txt', '''# ResearchHub AI - Backend Dependencies
# Milestone 1: Activity 1.1 - Create requirements.txt file
# Responsible: Chetan Galphat

fastapi==0.115.5
uvicorn[standard]==0.32.1
groq==0.11.0
sentence-transformers==3.3.1
numpy==1.26.4
sqlalchemy==2.0.36
alembic==1.14.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
pydantic[email]==2.10.3
pydantic-settings==2.6.1
httpx==0.27.0
python-dotenv==1.0.1
scikit-learn==1.5.2
''')

# .env.example - Milestone 2: Activity 2.2 (Chetan Galphat)
write_file('.env.example', '''# ResearchHub AI - Environment Variables
# Milestone 2: Activity 2.2 - Configure API credentials
# Responsible: Chetan Galphat
# Copy this file to .env and fill in your values

GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_super_secret_jwt_key_here_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./researchhub.db
BACKEND_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000/api
''')

# backend/app/core/config.py - Milestone 2: Activity 2.2 (Chetan Galphat)
write_file('backend/app/core/config.py', '''# ResearchHub AI - Configuration Settings
# Milestone 2: Activity 2.2 - Configure API credentials
# Responsible: Chetan Galphat

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str = "your_groq_api_key_here"
    
    # JWT Security Configuration
    secret_key: str = "your_super_secret_jwt_key_here_min_32_chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    database_url: str = "sqlite:///./researchhub.db"
    
    # CORS Configuration
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cache and return application settings."""
    return Settings()


settings = get_settings()
''')


# backend/app/core/security.py - Milestone 3: Activity 3.1 (Abhishek Kumar)
write_file('backend/app/core/security.py', '''# ResearchHub AI - Security Utilities
# Milestone 3: Activity 3.1 - Build authentication endpoints
# Responsible: Abhishek Kumar (TeamLead)

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with optional expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
''')


# backend/app/database.py - Milestone 3 (Abhishek Kumar)
write_file('backend/app/database.py', '''# ResearchHub AI - Database Configuration
# Milestone 3: Backend Development
# Responsible: Abhishek Kumar (TeamLead)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')


# backend/app/models/user.py - Milestone 3 (Abhishek Kumar)
write_file('backend/app/models/user.py', '''# ResearchHub AI - User Database Model
# Milestone 3: Activity 3.1 - Authentication
# Responsible: Abhishek Kumar (TeamLead)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base


class User(Base):
    """User model for authentication and workspace ownership."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workspaces = relationship("Workspace", back_populates="owner", cascade="all, delete-orphan")
''')

# backend/app/models/workspace.py
write_file('backend/app/models/workspace.py', '''# ResearchHub AI - Workspace Database Model
# Milestone 3: Backend Development
# Responsible: Prashant Dwivedi

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base


class Workspace(Base):
    """Workspace model for organizing research papers."""
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="workspaces")
    papers = relationship("Paper", back_populates="workspace", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="workspace", cascade="all, delete-orphan")
''')


# backend/app/models/paper.py
write_file('backend/app/models/paper.py', '''# ResearchHub AI - Research Paper Database Model
# Milestone 3: Activity 3.2 - Paper search API
# Responsible: Prashant Dwivedi

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base


class Paper(Base):
    """Research paper model for imported papers in workspaces."""
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, nullable=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=True)
    abstract = Column(Text, nullable=True)
    published_date = Column(String, nullable=True)
    url = Column(String, nullable=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", back_populates="papers")
''')

# backend/app/models/chat.py
write_file('backend/app/models/chat.py', '''# ResearchHub AI - Chat History Database Model
# Milestone 3: Activity 3.3 - AI chatbot endpoint
# Responsible: Aditya Singh

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base


class ChatHistory(Base):
    """Chat history model for storing AI conversation history."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", back_populates="chat_history")
''')

# backend/app/models/__init__.py
write_file('backend/app/models/__init__.py', '''# ResearchHub AI - Models Package
from backend.app.models.user import User
from backend.app.models.workspace import Workspace
from backend.app.models.paper import Paper
from backend.app.models.chat import ChatHistory

__all__ = ["User", "Workspace", "Paper", "ChatHistory"]
''')


# ============ SCHEMAS ============
write_file('backend/app/schemas/__init__.py', '')

write_file('backend/app/schemas/user.py', '''# ResearchHub AI - User Pydantic Schemas
# Milestone 3: Activity 3.1 - Authentication
# Responsible: Abhishek Kumar (TeamLead)

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str
''')

write_file('backend/app/schemas/workspace.py', '''# ResearchHub AI - Workspace Pydantic Schemas
# Milestone 3: Backend Development
# Responsible: Prashant Dwivedi

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceResponse(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
''')

write_file('backend/app/schemas/paper.py', '''# ResearchHub AI - Paper Pydantic Schemas
# Milestone 3: Activity 3.2 - Paper Search API
# Responsible: Prashant Dwivedi

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaperBase(BaseModel):
    title: str
    authors: Optional[str] = None
    abstract: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[str] = None
    arxiv_id: Optional[str] = None


class PaperImport(PaperBase):
    workspace_id: int


class PaperResponse(PaperBase):
    id: int
    workspace_id: int
    imported_at: datetime

    class Config:
        from_attributes = True


class ArxivSearchResult(BaseModel):
    arxiv_id: str
    title: str
    authors: str
    abstract: str
    published: str
    url: str
''')

write_file('backend/app/schemas/chat.py', '''# ResearchHub AI - Chat Pydantic Schemas
# Milestone 3: Activity 3.3 - AI Chatbot
# Responsible: Aditya Singh

from pydantic import BaseModel
from datetime import datetime
from typing import List


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    workspace_id: int
    message: str


class ChatResponse(BaseModel):
    answer: str
    workspace_id: int


class ChatHistoryResponse(BaseModel):
    id: int
    workspace_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
''')


# ============ SERVICES ============
write_file('backend/app/services/__init__.py', '')

# Groq AI Service - Milestone 2: Activity 2.3 (Abhishek Kumar)
write_file('backend/app/services/groq_service.py', '''# ResearchHub AI - Groq LLM Service
# Milestone 2: Activity 2.3 - Initialize Groq client and model
# Milestone 3: Activity 3.3 - AI Chatbot endpoint
# Milestone 5: Activity 5.1 - Research paper analysis
# Responsible: Abhishek Kumar (TeamLead)

from groq import Groq
from typing import List
from backend.app.core.config import settings

# Initialize Groq client with API key
# Temperature 0.3 for precise research analysis
client = Groq(api_key=settings.groq_api_key)
MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.3


def get_ai_response(messages: List[dict], context: str = "") -> str:
    """
    Get AI response from Groq Llama 3.3 70B model.
    Uses workspace paper context for grounded responses.
    """
    system_prompt = """You are ResearchHub AI, an intelligent research assistant specialized 
    in analyzing and synthesizing academic research papers. You provide accurate, 
    well-structured answers based on the research papers in the user\'s workspace.
    Always cite specific papers when referencing findings."""
    
    if context:
        system_prompt += f"\n\nResearch papers in workspace:\n{context}"
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        temperature=TEMPERATURE,
        max_tokens=2048
    )
    
    return response.choices[0].message.content
''')

# Embedding Service - Milestone 5 (Aditya Singh)
write_file('backend/app/services/embedding_service.py', '''# ResearchHub AI - Vector Embedding Service
# Milestone 5: Activity 5.1 - Research paper analysis with vector embeddings
# Responsible: Aditya Singh

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple

# Initialize the embedding model (multilingual support)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> List[float]:
    """Convert text to vector embedding using Sentence Transformers."""
    embedding = model.encode(text)
    return embedding.tolist()


def get_relevant_context(query: str, papers: List[dict], top_k: int = 3) -> str:
    """
    Find most relevant papers for a query using cosine similarity.
    Returns formatted context string for LLM consumption.
    """
    if not papers:
        return ""
    
    # Encode the query
    query_embedding = model.encode(query)
    
    # Encode all paper abstracts
    paper_texts = [
        f"{p.get(\'title\', \'\')} {p.get(\'abstract\', \'\')}"
        for p in papers
    ]
    paper_embeddings = model.encode(paper_texts)
    
    # Compute cosine similarities
    similarities = np.dot(paper_embeddings, query_embedding) / (
        np.linalg.norm(paper_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-10
    )
    
    # Get top-k most relevant papers
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    context_parts = []
    for idx in top_indices:
        paper = papers[idx]
        context_parts.append(
            f"Title: {paper.get(\'title\', \'Unknown\')}\n"
            f"Authors: {paper.get(\'authors\', \'Unknown\')}\n"
            f"Abstract: {paper.get(\'abstract\', \'No abstract\')}\n"
        )
    
    return "\n---\n".join(context_parts)
''')

# ArXiv Search Service - Milestone 3: Activity 3.2 (Prashant Dwivedi)
write_file('backend/app/services/arxiv_service.py', '''# ResearchHub AI - ArXiv Paper Search Service
# Milestone 3: Activity 3.2 - Implement paper search API
# Responsible: Prashant Dwivedi

import httpx
from typing import List
from backend.app.schemas.paper import ArxivSearchResult

ARXIV_API_URL = "https://export.arxiv.org/api/query"


async def search_arxiv(query: str, max_results: int = 10) -> List[ArxivSearchResult]:
    """
    Search ArXiv API for research papers matching the query.
    Returns structured list of paper metadata.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ARXIV_API_URL, params=params, timeout=30.0)
        response.raise_for_status()
    
    # Parse XML response
    return _parse_arxiv_response(response.text)


def _parse_arxiv_response(xml_text: str) -> List[ArxivSearchResult]:
    """Parse ArXiv XML response into structured paper data."""
    import xml.etree.ElementTree as ET
    
    root = ET.fromstring(xml_text)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    
    for entry in root.findall("atom:entry", namespace):
        arxiv_id_url = entry.find("atom:id", namespace)
        title = entry.find("atom:title", namespace)
        summary = entry.find("atom:summary", namespace)
        published = entry.find("atom:published", namespace)
        
        # Get authors
        authors = entry.findall("atom:author", namespace)
        author_names = ", ".join(
            [a.find("atom:name", namespace).text for a in authors if a.find("atom:name", namespace) is not None]
        )
        
        if arxiv_id_url is not None and title is not None:
            arxiv_url = arxiv_id_url.text.strip()
            arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else arxiv_url
            
            papers.append(ArxivSearchResult(
                arxiv_id=arxiv_id,
                title=" ".join(title.text.strip().split()),
                authors=author_names,
                abstract=summary.text.strip() if summary is not None else "",
                published=published.text[:10] if published is not None else "",
                url=arxiv_url
            ))
    
    return papers
''')


# ============ ROUTERS ============
write_file('backend/app/routers/__init__.py', '')

# Auth Router - Milestone 3: Activity 3.1 (Abhishek Kumar)
write_file('backend/app/routers/auth.py', '''# ResearchHub AI - Authentication Router
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
    user = db.query(User).filter(User.username == form_data.username).first()
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


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user
''')


# Papers Router - Milestone 3: Activity 3.2 (Prashant Dwivedi)
write_file('backend/app/routers/papers.py', '''# ResearchHub AI - Papers Router
# Milestone 3: Activity 3.2 - Implement paper search API
# Responsible: Prashant Dwivedi

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models.paper import Paper
from backend.app.models.workspace import Workspace
from backend.app.models.user import User
from backend.app.schemas.paper import PaperImport, PaperResponse, ArxivSearchResult
from backend.app.services.arxiv_service import search_arxiv
from backend.app.routers.auth import get_current_user

router = APIRouter(prefix="/papers", tags=["Papers"])


@router.get("/search", response_model=List[ArxivSearchResult])
async def search_papers(query: str, max_results: int = 10, current_user: User = Depends(get_current_user)):
    """Search ArXiv for research papers matching the query."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    results = await search_arxiv(query, max_results)
    return results


@router.post("/import", response_model=PaperResponse)
def import_paper(paper_data: PaperImport, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Import a paper into a workspace with one click."""
    # Verify workspace belongs to user
    workspace = db.query(Workspace).filter(
        Workspace.id == paper_data.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Create paper record
    paper = Paper(
        title=paper_data.title,
        authors=paper_data.authors,
        abstract=paper_data.abstract,
        published_date=paper_data.published_date,
        url=paper_data.url,
        arxiv_id=paper_data.arxiv_id,
        workspace_id=paper_data.workspace_id
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


@router.get("/workspace/{workspace_id}", response_model=List[PaperResponse])
def get_workspace_papers(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all papers in a specific workspace."""
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace.papers


@router.delete("/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a paper from a workspace."""
    paper = db.query(Paper).join(Workspace).filter(
        Paper.id == paper_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    db.delete(paper)
    db.commit()
    return {"message": "Paper deleted successfully"}
''')


# Chatbot Router - Milestone 3: Activity 3.3 (Aditya Singh)
write_file('backend/app/routers/chatbot.py', '''# ResearchHub AI - AI Chatbot Router
# Milestone 3: Activity 3.3 - Build AI chatbot endpoint
# Milestone 5: Activity 5.1 - Research paper analysis functions
# Responsible: Aditya Singh

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models.workspace import Workspace
from backend.app.models.user import User
from backend.app.models.chat import ChatHistory
from backend.app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from backend.app.services.groq_service import get_ai_response
from backend.app.services.embedding_service import get_relevant_context
from backend.app.routers.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])


@router.post("/", response_model=ChatResponse)
def chat_with_ai(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the AI chatbot.
    The chatbot uses workspace papers for context-aware responses.
    """
    # Verify workspace ownership
    workspace = db.query(Workspace).filter(
        Workspace.id == chat_request.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Get papers for context
    papers = [
        {"title": p.title, "abstract": p.abstract, "authors": p.authors}
        for p in workspace.papers
    ]
    
    # Get relevant context using vector embeddings
    context = get_relevant_context(chat_request.message, papers) if papers else ""
    
    # Get conversation history for this workspace
    history = db.query(ChatHistory).filter(
        ChatHistory.workspace_id == chat_request.workspace_id
    ).order_by(ChatHistory.created_at.desc()).limit(10).all()
    
    messages = [
        {"role": h.role, "content": h.content}
        for h in reversed(history)
    ]
    messages.append({"role": "user", "content": chat_request.message})
    
    # Get AI response from Groq
    answer = get_ai_response(messages, context)
    
    # Save to chat history
    db.add(ChatHistory(workspace_id=chat_request.workspace_id, role="user", content=chat_request.message))
    db.add(ChatHistory(workspace_id=chat_request.workspace_id, role="assistant", content=answer))
    db.commit()
    
    return ChatResponse(answer=answer, workspace_id=chat_request.workspace_id)


@router.get("/history/{workspace_id}", response_model=List[ChatHistoryResponse])
def get_chat_history(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get full chat history for a workspace."""
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace.chat_history


@router.delete("/history/{workspace_id}")
def clear_chat_history(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear all chat history for a workspace."""
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    db.query(ChatHistory).filter(ChatHistory.workspace_id == workspace_id).delete()
    db.commit()
    return {"message": "Chat history cleared"}
''')

# Workspaces Router - Milestone 3 (Prashant Dwivedi)
write_file('backend/app/routers/workspaces.py', '''# ResearchHub AI - Workspaces Router
# Milestone 3: Backend Development - Workspace Management
# Responsible: Prashant Dwivedi

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models.workspace import Workspace
from backend.app.models.user import User
from backend.app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from backend.app.routers.auth import get_current_user

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("/", response_model=WorkspaceResponse)
def create_workspace(workspace: WorkspaceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new research workspace for the current user."""
    new_workspace = Workspace(
        name=workspace.name,
        description=workspace.description,
        owner_id=current_user.id
    )
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return new_workspace


@router.get("/", response_model=List[WorkspaceResponse])
def list_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all workspaces owned by the current user."""
    return db.query(Workspace).filter(Workspace.owner_id == current_user.id).all()


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific workspace by ID."""
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id, Workspace.owner_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace


@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a workspace and all its papers."""
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id, Workspace.owner_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    db.delete(workspace)
    db.commit()
    return {"message": "Workspace deleted"}
''')


# main.py - Milestone 3 + Milestone 6: Activity 6.1 (All team)
write_file('backend/app/main.py', '''# ResearchHub AI - FastAPI Main Application
# Milestone 3: Backend Development with FastAPI
# Milestone 6: Activity 6.1 - Running the Backend
# Responsible: Abhishek Kumar (TeamLead) - Overall Architecture

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base

# Import all models to create tables
from backend.app.models import User, Workspace, Paper, ChatHistory

# Import routers
from backend.app.routers import auth, papers, chatbot, workspaces


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - creates database tables on startup."""
    # Create all database tables
    Base.metadata.create_all(bind=engine)
    print("ResearchHub AI Backend Started!")
    yield
    print("ResearchHub AI Backend Stopped.")


# Initialize FastAPI application
app = FastAPI(
    title="ResearchHub AI",
    description="Intelligent Research Paper Management and Analysis System using Agentic AI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - allows React frontend (port 3000) to communicate with backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers under /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(papers.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")
app.include_router(workspaces.router, prefix="/api")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "ResearchHub AI Backend is running!", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "ResearchHub AI"}
''')

# backend/app/__init__.py
write_file('backend/app/__init__.py', '')
write_file('backend/app/core/__init__.py', '')


# ============ FRONTEND FILES ============
# package.json - Milestone 4: Activity 4.1 (Chetan Galphat)
write_file('frontend/package.json', '''{
  "name": "researchhub-ai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "start": "vite"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0",
    "axios": "^1.7.9",
    "lucide-react": "^0.468.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.16",
    "typescript": "^5.6.3",
    "vite": "^6.0.3"
  }
}
''')

# vite.config.ts
write_file('frontend/vite.config.ts', '''// ResearchHub AI - Vite Configuration
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
''')

# tsconfig.json
write_file('frontend/tsconfig.json', '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{"path": "./tsconfig.node.json"}]
}
''')

write_file('frontend/tsconfig.node.json', '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
''')

# tailwind.config.js
write_file('frontend/tailwind.config.js', '''/** @type {import(\'tailwindcss\').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 50: "#eff6ff", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8" },
      },
    },
  },
  plugins: [],
};
''')

write_file('frontend/postcss.config.js', '''export default {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
''')

# index.html
write_file('frontend/index.html', '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ResearchHub AI</title>
    <meta name="description" content="Intelligent Research Paper Management and Analysis System" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')


# Frontend React/TypeScript files - Milestone 4: Activity 4.1 (Chetan Galphat)
write_file('frontend/src/main.tsx', '''// ResearchHub AI - React Application Entry Point
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')

write_file('frontend/src/index.css', '''/* ResearchHub AI - Global Styles */
/* Milestone 4: Activity 4.1 - Frontend Styling with Tailwind CSS */
/* Responsible: Chetan Galphat */
@tailwind base;
@tailwind components;
@tailwind utilities;

body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
''')

write_file('frontend/src/App.tsx', '''// ResearchHub AI - Main App Component with Routing
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Dashboard from "./pages/Dashboard";
import WorkspaceList from "./pages/WorkspaceList";
import WorkspaceDetail from "./pages/WorkspaceDetail";
import SearchPage from "./pages/SearchPage";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/workspaces" element={<PrivateRoute><WorkspaceList /></PrivateRoute>} />
          <Route path="/workspaces/:id" element={<PrivateRoute><WorkspaceDetail /></PrivateRoute>} />
          <Route path="/search" element={<PrivateRoute><SearchPage /></PrivateRoute>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
''')


# AuthContext - Milestone 4 (Chetan Galphat)
write_file('frontend/src/context/AuthContext.tsx', '''// ResearchHub AI - Authentication Context
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

interface User { id: number; username: string; email: string; full_name?: string; }
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      axios.get(`${API_URL}/auth/me`)
        .then(res => setUser(res.data))
        .catch(() => { setToken(null); localStorage.removeItem("token"); });
    }
  }, [token]);

  const login = async (username: string, password: string) => {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    const res = await axios.post(`${API_URL}/auth/login`, form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    const newToken = res.data.access_token;
    setToken(newToken);
    localStorage.setItem("token", newToken);
    axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;
    const userRes = await axios.get(`${API_URL}/auth/me`);
    setUser(userRes.data);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    delete axios.defaults.headers.common["Authorization"];
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
''')

# API Service
write_file('frontend/src/services/api.ts', '''// ResearchHub AI - API Service Layer
// Milestone 4: Activity 4.1 - Frontend Services
// Responsible: Chetan Galphat

import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const api = axios.create({ baseURL: API_URL });

// Set auth token from localStorage on startup
const token = localStorage.getItem("token");
if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

// Workspaces
export const getWorkspaces = () => api.get("/workspaces/");
export const createWorkspace = (name: string, description?: string) =>
  api.post("/workspaces/", { name, description });
export const deleteWorkspace = (id: number) => api.delete(`/workspaces/${id}`);

// Papers
export const searchPapers = (query: string, max?: number) =>
  api.get("/papers/search", { params: { query, max_results: max || 10 } });
export const importPaper = (paper: object) => api.post("/papers/import", paper);
export const getWorkspacePapers = (workspaceId: number) =>
  api.get(`/papers/workspace/${workspaceId}`);
export const deletePaper = (id: number) => api.delete(`/papers/${id}`);

// Chat
export const sendMessage = (workspace_id: number, message: string) =>
  api.post("/chat/", { workspace_id, message });
export const getChatHistory = (workspaceId: number) =>
  api.get(`/chat/history/${workspaceId}`);
export const clearChatHistory = (workspaceId: number) =>
  api.delete(`/chat/history/${workspaceId}`);
''')


# Components
write_file('frontend/src/components/PrivateRoute.tsx', '''// ResearchHub AI - Private Route Guard
// Milestone 4: Activity 4.1
// Responsible: Chetan Galphat

import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ReactNode } from "react";

export default function PrivateRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}
''')

write_file('frontend/src/components/Navbar.tsx', '''// ResearchHub AI - Navigation Bar Component
// Milestone 4: Activity 4.1
// Responsible: Chetan Galphat

import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate("/login"); };
  return (
    <nav className="bg-blue-700 text-white px-6 py-4 flex justify-between items-center shadow-lg">
      <Link to="/" className="text-xl font-bold">ResearchHub AI</Link>
      <div className="flex gap-4 items-center">
        <Link to="/workspaces" className="hover:text-blue-200">Workspaces</Link>
        <Link to="/search" className="hover:text-blue-200">Search Papers</Link>
        <span className="text-blue-200">{user?.username}</span>
        <button onClick={handleLogout} className="bg-blue-500 hover:bg-blue-400 px-3 py-1 rounded">Logout</button>
      </div>
    </nav>
  );
}
''')

# Pages
write_file('frontend/src/pages/LoginPage.tsx', '''// ResearchHub AI - Login Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError("");
    try {
      await login(username, password);
      navigate("/");
    } catch { setError("Invalid username or password"); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center text-blue-700 mb-6">ResearchHub AI</h1>
        <h2 className="text-xl font-semibold mb-4 text-center">Sign In</h2>
        {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)}
            className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)}
            className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
          <button type="submit" disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
        <p className="text-center mt-4 text-sm">No account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link></p>
      </div>
    </div>
  );
}
''')


write_file('frontend/src/pages/RegisterPage.tsx', '''// ResearchHub AI - Register Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", username: "", full_name: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const API = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError("");
    try {
      await axios.post(`${API}/auth/register`, form);
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center text-blue-700 mb-6">ResearchHub AI</h1>
        <h2 className="text-xl font-semibold mb-4 text-center">Create Account</h2>
        {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          {["full_name", "username", "email", "password"].map(field => (
            <input key={field} type={field === "password" ? "password" : "text"}
              placeholder={field.replace("_", " ").replace(/\\b\\w/g, c => c.toUpperCase())}
              value={(form as any)[field]} onChange={e => setForm({ ...form, [field]: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
              required={field !== "full_name"} />
          ))}
          <button type="submit" disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        <p className="text-center mt-4 text-sm">Have account? <Link to="/login" className="text-blue-600 hover:underline">Sign In</Link></p>
      </div>
    </div>
  );
}
''')

write_file('frontend/src/pages/Dashboard.tsx', '''// ResearchHub AI - Dashboard Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome, {user?.full_name || user?.username}!</h1>
        <p className="text-gray-500 mb-8">ResearchHub AI - Your intelligent research paper assistant</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/workspaces" className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition border border-gray-100">
            <h3 className="text-lg font-semibold text-blue-700 mb-2">My Workspaces</h3>
            <p className="text-gray-500 text-sm">Organize your research papers into project workspaces</p>
          </Link>
          <Link to="/search" className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition border border-gray-100">
            <h3 className="text-lg font-semibold text-green-700 mb-2">Search Papers</h3>
            <p className="text-gray-500 text-sm">Search ArXiv for research papers and import them</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
''')


write_file('frontend/src/pages/WorkspaceList.tsx', '''// ResearchHub AI - Workspace List Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getWorkspaces, createWorkspace, deleteWorkspace } from "../services/api";

export default function WorkspaceList() {
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [name, setName] = useState(""); const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchWorkspaces = async () => {
    const res = await getWorkspaces(); setWorkspaces(res.data);
  };
  useEffect(() => { fetchWorkspaces(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); if (!name.trim()) return;
    setLoading(true);
    await createWorkspace(name, desc); setName(""); setDesc("");
    await fetchWorkspaces(); setLoading(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this workspace?")) return;
    await deleteWorkspace(id); fetchWorkspaces();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">My Workspaces</h1>
        <form onSubmit={handleCreate} className="bg-white p-5 rounded-xl shadow mb-8 flex gap-3 flex-wrap">
          <input placeholder="Workspace name" value={name} onChange={e => setName(e.target.value)}
            className="border rounded-lg px-3 py-2 flex-1 min-w-40 focus:ring-2 focus:ring-blue-400 focus:outline-none" required />
          <input placeholder="Description (optional)" value={desc} onChange={e => setDesc(e.target.value)}
            className="border rounded-lg px-3 py-2 flex-1 min-w-40 focus:ring-2 focus:ring-blue-400 focus:outline-none" />
          <button type="submit" disabled={loading}
            className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? "Creating..." : "Create"}
          </button>
        </form>
        <div className="grid gap-4">
          {workspaces.map(ws => (
            <div key={ws.id} className="bg-white p-5 rounded-xl shadow flex justify-between items-center">
              <div>
                <Link to={`/workspaces/${ws.id}`} className="font-semibold text-blue-700 hover:underline">{ws.name}</Link>
                {ws.description && <p className="text-gray-500 text-sm mt-1">{ws.description}</p>}
              </div>
              <button onClick={() => handleDelete(ws.id)} className="text-red-500 hover:text-red-700 text-sm">Delete</button>
            </div>
          ))}
          {workspaces.length === 0 && <p className="text-gray-500 text-center py-8">No workspaces yet. Create your first one above!</p>}
        </div>
      </main>
    </div>
  );
}
''')


write_file('frontend/src/pages/WorkspaceDetail.tsx', '''// ResearchHub AI - Workspace Detail with AI Chat
// Milestone 4: Activity 4.1 - Frontend Development
// Milestone 5: Research Paper Analysis UI
// Responsible: Chetan Galphat

import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getWorkspacePapers, deletePaper, sendMessage, getChatHistory } from "../services/api";

export default function WorkspaceDetail() {
  const { id } = useParams<{ id: string }>();
  const workspaceId = parseInt(id!);
  const [papers, setPapers] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  const fetchData = async () => {
    const [papersRes, chatRes] = await Promise.all([
      getWorkspacePapers(workspaceId),
      getChatHistory(workspaceId)
    ]);
    setPapers(papersRes.data);
    setMessages(chatRes.data);
  };

  useEffect(() => { fetchData(); }, [workspaceId]);
  useEffect(() => { chatRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault(); if (!input.trim()) return;
    const userMsg = input; setInput(""); setLoading(true);
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    try {
      const res = await sendMessage(workspaceId, userMsg);
      setMessages(prev => [...prev, { role: "assistant", content: res.data.answer }]);
    } catch { setMessages(prev => [...prev, { role: "assistant", content: "Error getting response" }]); }
    setLoading(false);
  };

  const handleDeletePaper = async (paperId: number) => {
    if (!confirm("Remove this paper?")) return;
    await deletePaper(paperId); fetchData();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-bold mb-4 text-gray-800">Papers ({papers.length})</h2>
          <div className="space-y-3 max-h-[70vh] overflow-y-auto">
            {papers.map(p => (
              <div key={p.id} className="bg-white p-4 rounded-lg shadow">
                <div className="flex justify-between">
                  <a href={p.url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 hover:underline text-sm">{p.title}</a>
                  <button onClick={() => handleDeletePaper(p.id)} className="text-red-400 hover:text-red-600 text-xs ml-2">Remove</button>
                </div>
                <p className="text-gray-500 text-xs mt-1">{p.authors}</p>
              </div>
            ))}
            {papers.length === 0 && <p className="text-gray-400 text-center py-6">No papers yet. Import from Search.</p>}
          </div>
        </div>
        <div className="flex flex-col">
          <h2 className="text-xl font-bold mb-4 text-gray-800">AI Research Assistant</h2>
          <div className="bg-white rounded-xl shadow flex-1 flex flex-col" style={{minHeight: "400px"}}>
            <div className="flex-1 p-4 overflow-y-auto space-y-3 max-h-96">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-xs lg:max-w-sm px-4 py-2 rounded-2xl text-sm ${m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-800"}`}>
                    {m.content}
                  </div>
                </div>
              ))}
              {loading && <div className="flex justify-start"><div className="bg-gray-100 px-4 py-2 rounded-2xl text-sm text-gray-500">Thinking...</div></div>}
              <div ref={chatRef} />
            </div>
            <form onSubmit={handleChat} className="p-4 border-t flex gap-2">
              <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about your papers..."
                className="flex-1 border rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400" />
              <button type="submit" disabled={loading || !input.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm hover:bg-blue-700 disabled:opacity-50">Send</button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
''')


write_file('frontend/src/pages/SearchPage.tsx', '''// ResearchHub AI - Search Papers Page
// Milestone 4: Activity 4.1 - Frontend Development
// Milestone 3: Activity 3.2 - Paper Search Integration
// Responsible: Chetan Galphat

import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import { searchPapers, importPaper, getWorkspaces } from "../services/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [selectedWs, setSelectedWs] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => { getWorkspaces().then(res => {
    setWorkspaces(res.data); if (res.data.length > 0) setSelectedWs(res.data[0].id);
  }); }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault(); if (!query.trim()) return;
    setLoading(true); setResults([]);
    try { const res = await searchPapers(query, 10); setResults(res.data); }
    catch { setMessage("Search failed. Try again."); }
    setLoading(false);
  };

  const handleImport = async (paper: any) => {
    if (!selectedWs) { setMessage("Select a workspace first"); return; }
    setImporting(paper.arxiv_id);
    try {
      await importPaper({ ...paper, workspace_id: selectedWs });
      setMessage(`"${paper.title.slice(0, 40)}..." imported!`);
    } catch { setMessage("Import failed"); }
    setImporting(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">Search Research Papers</h1>
        {message && <p className="mb-4 text-green-600 bg-green-50 px-4 py-2 rounded-lg text-sm">{message}</p>}
        <div className="bg-white p-5 rounded-xl shadow mb-6">
          <form onSubmit={handleSearch} className="flex gap-3 mb-4">
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search ArXiv papers..."
              className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
            <button type="submit" disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {loading ? "Searching..." : "Search"}
            </button>
          </form>
          {workspaces.length > 0 && (
            <div className="flex items-center gap-3">
              <label className="text-sm text-gray-600">Import to:</label>
              <select value={selectedWs} onChange={e => setSelectedWs(parseInt(e.target.value))}
                className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400">
                {workspaces.map(ws => <option key={ws.id} value={ws.id}>{ws.name}</option>)}
              </select>
            </div>
          )}
        </div>
        <div className="space-y-4">
          {results.map(paper => (
            <div key={paper.arxiv_id} className="bg-white p-5 rounded-xl shadow">
              <div className="flex justify-between gap-4">
                <div className="flex-1">
                  <a href={paper.url} target="_blank" rel="noopener noreferrer"
                    className="font-semibold text-blue-700 hover:underline">{paper.title}</a>
                  <p className="text-gray-500 text-sm mt-1">{paper.authors}</p>
                  <p className="text-gray-600 text-sm mt-2 line-clamp-3">{paper.abstract}</p>
                  <p className="text-gray-400 text-xs mt-1">{paper.published}</p>
                </div>
                <button onClick={() => handleImport(paper)} disabled={importing === paper.arxiv_id}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 text-sm whitespace-nowrap self-start">
                  {importing === paper.arxiv_id ? "Importing..." : "Import"}
                </button>
              </div>
            </div>
          ))}
          {results.length === 0 && !loading && <p className="text-center text-gray-400 py-8">Enter a query to search ArXiv papers</p>}
        </div>
      </main>
    </div>
  );
}
''')

# .env file for frontend
write_file('frontend/.env.example', '''VITE_API_URL=http://localhost:8000/api
''')


# .gitignore
write_file('.gitignore', '''# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/

# Environment
.env
*.env

# Database
*.db
*.sqlite

# Node.js
node_modules/
dist/
.DS_Store

# IDE
.vscode/
.idea/
*.swp

# Build artifacts
frontend/dist/
frontend/build/
''')

# docker-compose.yml
write_file('docker-compose.yml', '''# ResearchHub AI - Docker Compose
# Milestone 6: Activity 6.1, 6.2 - Running Backend and Frontend
# Responsible: All Team Members

version: "3.8"
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:///./researchhub.db
    volumes: ["./backend:/app"]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
    environment:
      - VITE_API_URL=http://localhost:8000/api
''')

# backend/Dockerfile
write_file('backend/Dockerfile', '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# frontend/Dockerfile
write_file('frontend/Dockerfile', '''FROM node:20-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
''')


# README.md
write_file('README.md', '''# ResearchHub AI
## Intelligent Research Paper Management and Analysis System using Agentic AI

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Frontend-React+TypeScript-61DAFB?style=flat-square)
![Tech Stack](https://img.shields.io/badge/AI-Groq+Llama3.3+70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

ResearchHub AI is an intelligent, agentic AI-powered research paper management platform.
Built using React and TypeScript for the frontend, FastAPI for backend processing, and
integrated with Groq LLM Llama 3.3 70B for advanced natural language understanding.

## Team Members

| Name | Role | Assigned Milestones/Tasks |
|------|------|---------------------------|
| Abhishek Kumar | TeamLead | Milestone 2 (Groq API), Milestone 3 Activity 3.1 (Auth), Backend Architecture |
| Chetan Galphat | Member | Milestone 1 (Pre-requisites), Milestone 2 Activity 2.2 (API Config), Milestone 4 (Frontend) |
| Prashant Dwivedi | Member | Milestone 3 Activity 3.2 (Paper Search API), Workspace Management |
| Aditya Singh | Member | Milestone 3 Activity 3.3 (AI Chatbot), Milestone 5 (Vector Embeddings) |
| Bhavin Suryavanshi | Member | Milestone 6 (Testing & Deployment), Documentation |

## Features

- **Paper Search**: Search ArXiv for research papers with metadata
- **One-Click Import**: Save papers to personal workspaces
- **AI Chatbot**: Ask questions about your research papers using Groq Llama 3.3 70B
- **Vector Search**: Semantic paper retrieval using Sentence Transformers
- **JWT Authentication**: Secure user accounts with bcrypt password hashing
- **Multiple Workspaces**: Organize papers by research topic

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Groq** - LLM inference with Llama 3.3 70B (temperature: 0.3)
- **Sentence Transformers** - Vector embeddings for semantic search
- **SQLAlchemy** - Database ORM with SQLite
- **python-jose** - JWT authentication
- **passlib[bcrypt]** - Password hashing
- **httpx** - Async HTTP client for ArXiv API

### Frontend
- **React 18** + **TypeScript** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router v6** - Client-side routing
- **Axios** - HTTP client

## Project Structure

```
ResearchHub-AI/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py      # Settings (Groq API, JWT)
│   │   │   └── security.py    # Password hashing, JWT tokens
│   │   ├── models/
│   │   │   ├── user.py        # User SQLAlchemy model
│   │   │   ├── workspace.py   # Workspace model
│   │   │   ├── paper.py       # Paper model
│   │   │   └── chat.py        # Chat history model
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── groq_service.py       # Groq LLM integration
│   │   │   ├── embedding_service.py  # Vector embeddings
│   │   │   └── arxiv_service.py      # ArXiv paper search
│   │   ├── routers/
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── papers.py      # Paper CRUD + search
│   │   │   ├── chatbot.py     # AI chat endpoints
│   │   │   └── workspaces.py  # Workspace management
│   │   ├── database.py        # SQLAlchemy setup
│   │   └── main.py            # FastAPI application entry
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── context/           # React Context (Auth)
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service layer
│   │   └── App.tsx            # Root component
│   ├── package.json
│   └── Dockerfile
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Groq API Key from https://console.groq.com

### Backend Setup (Milestone 1 & 2)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Activity 1.2)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies (Activity 1.1)
pip install -r requirements.txt

# Configure environment (Activity 2.2)
cp ../.env.example ../.env
# Edit .env and add your GROQ_API_KEY and SECRET_KEY

# Run the backend (Activity 6.1)
cd ..
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API docs available at: http://localhost:8000/docs

### Frontend Setup (Milestone 4 - Activity 4.1)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api

# Run the frontend (Activity 6.2)
npm run dev
```

Frontend available at: http://localhost:3000

### Docker Setup

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT token |
| GET | /api/auth/me | Get current user |
| GET | /api/workspaces/ | List workspaces |
| POST | /api/workspaces/ | Create workspace |
| GET | /api/papers/search?query= | Search ArXiv papers |
| POST | /api/papers/import | Import paper to workspace |
| POST | /api/chat/ | Chat with AI about papers |
| GET | /api/chat/history/{workspace_id} | Get chat history |

## License

MIT License - ResearchHub AI Team, 2026
''')

print('All files created successfully!')
print('Run: python setup.py')
