# ResearchHub AI - Chat History Database Model
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
