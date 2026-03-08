# ResearchHub AI - Papers Router
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
