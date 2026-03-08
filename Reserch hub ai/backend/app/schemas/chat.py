# ResearchHub AI - Chat Pydantic Schemas
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
