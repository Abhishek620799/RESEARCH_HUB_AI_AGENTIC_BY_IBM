# ResearchHub AI - Workspace Pydantic Schemas
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
