"""Vector search endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.models.user import User
from app.auth import get_current_active_user
from app.services.vector_service import vector_service
from pydantic import BaseModel

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    """Search request schema."""
    query: str
    course_id: Optional[str] = None
    top_k: int = 5


class SearchResult(BaseModel):
    """Search result schema."""
    doc_id: str
    text_snippet: str
    score: float
    source: dict


@router.post("/", response_model=List[SearchResult])
async def search_documents(
    request: SearchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Search documents using vector similarity."""
    try:
        results = await vector_service.search_similar_documents(
            query=request.query,
            document_type=None,
            limit=request.top_k
        )
        
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                doc_id=result["document_id"],
                text_snippet=result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                score=result["similarity"],
                source={
                    "file_id": result["metadata"].get("filename"),
                    "chapter_id": result["document_id"] if result["document_type"] == "chapter" else None,
                    "offset": 0  # Placeholder
                }
            ))
        
        return search_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/embeddings")
async def reindex_embeddings(
    file_id: Optional[str] = None,
    course_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Reindex embeddings for files or courses."""
    try:
        if file_id:
            # Reindex specific file
            await vector_service.index_upload_content(file_id)
            return {"message": f"File {file_id} reindexed successfully"}
        elif course_id:
            # Reindex course
            await vector_service.index_course_content(course_id)
            return {"message": f"Course {course_id} reindexed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either file_id or course_id must be provided"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reindexing failed: {str(e)}"
        )


@router.post("/courses/{course_id}/reindex")
async def reindex_course(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Reindex course embeddings."""
    try:
        await vector_service.index_course_content(course_id)
        return {"message": f"Course {course_id} reindexed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Course reindexing failed: {str(e)}"
        )
