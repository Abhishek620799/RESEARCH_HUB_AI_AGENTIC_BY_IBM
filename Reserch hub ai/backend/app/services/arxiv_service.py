# ResearchHub AI - ArXiv Paper Search Service
# Milestone 3: Activity 3.2 - Implement paper search API
# Responsible: Prashant Dwivedi

import httpx
from typing import List
from backend.app.schemas.paper import ArxivSearchResult

ARXIV_API_URL = "https://export.arxiv.org/api/query"


async def search_arxiv(query: str, max_results: int = 10) -> List[ArxivSearchResult]:
    """
    Search ArXiv API for research papers matching the query.
    Returns structured list of paper metadata.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ARXIV_API_URL, params=params, timeout=30.0)
        response.raise_for_status()
    
    # Parse XML response
    return _parse_arxiv_response(response.text)


def _parse_arxiv_response(xml_text: str) -> List[ArxivSearchResult]:
    """Parse ArXiv XML response into structured paper data."""
    import xml.etree.ElementTree as ET
    
    root = ET.fromstring(xml_text)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    
    for entry in root.findall("atom:entry", namespace):
        arxiv_id_url = entry.find("atom:id", namespace)
        title = entry.find("atom:title", namespace)
        summary = entry.find("atom:summary", namespace)
        published = entry.find("atom:published", namespace)
        
        # Get authors
        authors = entry.findall("atom:author", namespace)
        author_names = ", ".join(
            [a.find("atom:name", namespace).text for a in authors if a.find("atom:name", namespace) is not None]
        )
        
        if arxiv_id_url is not None and title is not None:
            arxiv_url = arxiv_id_url.text.strip()
            arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else arxiv_url
            
            papers.append(ArxivSearchResult(
                arxiv_id=arxiv_id,
                title=" ".join(title.text.strip().split()),
                authors=author_names,
                abstract=summary.text.strip() if summary is not None else "",
                published=published.text[:10] if published is not None else "",
                url=arxiv_url
            ))
    
    return papers
