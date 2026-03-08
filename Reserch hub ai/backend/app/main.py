# ResearchHub AI - FastAPI Main Application
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
    # Create all database tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="ResearchHub AI",
    description="Intelligent Research Paper Management and Analysis System using Agentic AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - allow all origins so Codespace frontend can reach backend
# Bhavin Suryavanshi - Deployment configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routers
app.include_router(auth.router, prefix="/api")
app.include_router(papers.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")
app.include_router(workspaces.router, prefix="/api")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "ResearchHub AI API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    """Health check for deployment monitoring."""
    return {"status": "healthy"}
