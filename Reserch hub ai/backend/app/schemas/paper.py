# ResearchHub AI - Paper Pydantic Schemas
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
