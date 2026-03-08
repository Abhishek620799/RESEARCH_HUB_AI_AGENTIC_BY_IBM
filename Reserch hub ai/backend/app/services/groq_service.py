# ResearchHub AI - Groq LLM Service
# Milestone 2: Activity 2.3 - Initialize Groq client and API integration
# Milestone 3: Activity 3.3 - AI response generation
# Milestone 5: Activity 5.1 - Response streaming
# Responsible: Abhishek Kumar (TeamLead)

from groq import Groq
from typing import List
from backend.app.core.config import settings

# Initialize Groq client with API key from environment
# Temperature 0.3 for precise academic responses
client = Groq(api_key=settings.groq_api_key)
MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.3


def get_ai_response(messages: List[dict], context: str = "") -> str:
    """
    Get AI response from Groq Llama 3.3 70B model.
    Abhishek Kumar (TeamLead) - Core AI integration.
    """
    system_prompt = (
        "You are ResearchHub AI, an intelligent research assistant specialized "
        "in analyzing and synthesizing academic research papers. You provide accurate, "
        "well-structured answers based on the research papers in the user's workspace. "
        "Always cite specific papers when referencing findings."
    )

    if context:
        system_prompt = system_prompt + "\n\nResearch papers in workspace: " + context

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        temperature=TEMPERATURE,
        max_tokens=2048,
    )
    return response.choices[0].message.content


def get_paper_summary(abstract: str, title: str) -> str:
    """
    Generate a concise summary of a research paper.
    Abhishek Kumar (TeamLead) - Paper summarization.
    """
    prompt = "Summarize this research paper in 3-4 sentences. Title: " + title + ". Abstract: " + abstract
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=512,
    )
    return response.choices[0].message.content


def extract_key_concepts(text: str) -> List[str]:
    """
    Extract key concepts from paper text using Groq.
    Aditya Singh - Key concept extraction for embeddings.
    """
    prompt = "Extract 5-10 key concepts from this research text as a comma-separated list: " + text[:2000]
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=256,
    )
    concepts_text = response.choices[0].message.content
    return [c.strip() for c in concepts_text.split(",") if c.strip()]
