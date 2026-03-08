# ResearchHub AI - Workspace Database Model
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
