# ResearchHub AI - Workspaces Router
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
