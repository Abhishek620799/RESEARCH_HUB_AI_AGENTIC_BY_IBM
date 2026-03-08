# ResearchHub AI - Research Paper Database Model
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
