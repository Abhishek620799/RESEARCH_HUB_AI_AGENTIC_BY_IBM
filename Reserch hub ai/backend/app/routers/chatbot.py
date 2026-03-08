# ResearchHub AI - AI Chatbot Router
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
    try:
        context = get_relevant_context(chat_request.message, papers) if papers else ""
    except Exception:
        context = ""

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
    try:
        answer = get_ai_response(messages, context)
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            answer = "AI service is unavailable: Groq API key not configured. Please set GROQ_API_KEY in your .env file."
        else:
            answer = "I encountered an error processing your request. Please try again. Error: " + error_msg[:200]

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
