# ResearchHub AI
## Intelligent Research Paper Management and Analysis System using Agentic AI

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Frontend-React+TypeScript-61DAFB?style=flat-square)
![Tech Stack](https://img.shields.io/badge/AI-Groq+Llama3.3+70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

ResearchHub AI is an intelligent, agentic AI-powered research paper management platform.
Built using React and TypeScript for the frontend, FastAPI for backend processing, and
integrated with Groq LLM Llama 3.3 70B for advanced natural language understanding.

## Team Members

| Name | Role | Assigned Milestones/Tasks |
|------|------|---------------------------|
| Abhishek Kumar | TeamLead | Milestone 2 (Groq API), Milestone 3 Activity 3.1 (Auth), Backend Architecture |
| Chetan Galphat | Member | Milestone 1 (Pre-requisites), Milestone 2 Activity 2.2 (API Config), Milestone 4 (Frontend) |
| Prashant Dwivedi | Member | Milestone 3 Activity 3.2 (Paper Search API), Workspace Management |
| Aditya Singh | Member | Milestone 3 Activity 3.3 (AI Chatbot), Milestone 5 (Vector Embeddings) |
| Bhavin Suryavanshi | Member | Milestone 6 (Testing & Deployment), Documentation |

## Features

- **Paper Search**: Search ArXiv for research papers with metadata
- **One-Click Import**: Save papers to personal workspaces
- **AI Chatbot**: Ask questions about your research papers using Groq Llama 3.3 70B
- **Vector Search**: Semantic paper retrieval using Sentence Transformers
- **JWT Authentication**: Secure user accounts with bcrypt password hashing
- **Multiple Workspaces**: Organize papers by research topic

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Groq** - LLM inference with Llama 3.3 70B (temperature: 0.3)
- **Sentence Transformers** - Vector embeddings for semantic search
- **SQLAlchemy** - Database ORM with SQLite
- **python-jose** - JWT authentication
- **passlib[bcrypt]** - Password hashing
- **httpx** - Async HTTP client for ArXiv API

### Frontend
- **React 18** + **TypeScript** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router v6** - Client-side routing
- **Axios** - HTTP client

## Project Structure

```
ResearchHub-AI/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py      # Settings (Groq API, JWT)
│   │   │   └── security.py    # Password hashing, JWT tokens
│   │   ├── models/
│   │   │   ├── user.py        # User SQLAlchemy model
│   │   │   ├── workspace.py   # Workspace model
│   │   │   ├── paper.py       # Paper model
│   │   │   └── chat.py        # Chat history model
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── groq_service.py       # Groq LLM integration
│   │   │   ├── embedding_service.py  # Vector embeddings
│   │   │   └── arxiv_service.py      # ArXiv paper search
│   │   ├── routers/
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── papers.py      # Paper CRUD + search
│   │   │   ├── chatbot.py     # AI chat endpoints
│   │   │   └── workspaces.py  # Workspace management
│   │   ├── database.py        # SQLAlchemy setup
│   │   └── main.py            # FastAPI application entry
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── context/           # React Context (Auth)
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service layer
│   │   └── App.tsx            # Root component
│   ├── package.json
│   └── Dockerfile
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Groq API Key from https://console.groq.com

### Backend Setup (Milestone 1 & 2)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Activity 1.2)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (Activity 1.1)
pip install -r requirements.txt

# Configure environment (Activity 2.2)
cp ../.env.example ../.env
# Edit .env and add your GROQ_API_KEY and SECRET_KEY

# Run the backend (Activity 6.1)
cd ..
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API docs available at: http://localhost:8000/docs

### Frontend Setup (Milestone 4 - Activity 4.1)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api

# Run the frontend (Activity 6.2)
npm run dev
```

Frontend available at: http://localhost:3000

### Docker Setup

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT token |
| GET | /api/auth/me | Get current user |
| GET | /api/workspaces/ | List workspaces |
| POST | /api/workspaces/ | Create workspace |
| GET | /api/papers/search?query= | Search ArXiv papers |
| POST | /api/papers/import | Import paper to workspace |
| POST | /api/chat/ | Chat with AI about papers |
| GET | /api/chat/history/{workspace_id} | Get chat history |

## License

MIT License - ResearchHub AI Team, 2026
