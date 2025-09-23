"""Vector search service for semantic search."""

from typing import List, Dict, Any, Optional
from pymongo import ASCENDING
from app.database import init_db
from app.models.course import Course, Chapter
from app.models.upload import Upload
from app.services.genai_service import genai_service


class VectorService:
    """Service for vector search and semantic operations."""
    
    def __init__(self):
        """Initialize vector service."""
        self.collection_name = "vector_embeddings"
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text."""
        try:
            # For now, we'll use a simple text-based similarity
            # In production, you'd use a proper embedding model
            return await genai_service.generate_embeddings(text)
        except Exception as e:
            raise Exception(f"Failed to create embedding: {str(e)}")
    
    async def store_document_embedding(
        self, 
        document_id: str, 
        document_type: str, 
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store document embedding in vector database."""
        try:
            embedding = await self.create_embedding(content)
            
            # Store in MongoDB (you can replace this with a dedicated vector DB)
            from app.database import init_db
            from motor.motor_asyncio import AsyncIOMotorClient
            from app.config import settings
            
            client = AsyncIOMotorClient(settings.mongodb_url)
            db = client[settings.database_name]
            collection = db[self.collection_name]
            
            document = {
                "document_id": document_id,
                "document_type": document_type,
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {}
            }
            
            await collection.insert_one(document)
            return True
        except Exception as e:
            raise Exception(f"Failed to store embedding: {str(e)}")
    
    async def search_similar_documents(
        self, 
        query: str, 
        document_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity."""
        try:
            query_embedding = await self.create_embedding(query)
            
            # For now, we'll do a simple text search
            # In production, you'd use proper vector similarity search
            from app.database import init_db
            from motor.motor_asyncio import AsyncIOMotorClient
            from app.config import settings
            
            client = AsyncIOMotorClient(settings.mongodb_url)
            db = client[settings.database_name]
            collection = db[self.collection_name]
            
            # Simple text search for now
            search_filter = {}
            if document_type:
                search_filter["document_type"] = document_type
            
            cursor = collection.find(search_filter).limit(limit)
            results = []
            
            async for doc in cursor:
                results.append({
                    "document_id": doc["document_id"],
                    "document_type": doc["document_type"],
                    "content": doc["content"],
                    "metadata": doc.get("metadata", {}),
                    "similarity": 0.8  # Mock similarity score
                })
            
            return results
        except Exception as e:
            raise Exception(f"Failed to search documents: {str(e)}")
    
    async def index_course_content(self, course_id: str) -> bool:
        """Index course content for vector search."""
        try:
            # Get course and chapters
            course = await Course.get(course_id)
            if not course:
                return False
            
            chapters = await Chapter.find(Chapter.course_id == course_id).to_list()
            
            # Index course description
            if course.description:
                await self.store_document_embedding(
                    document_id=course_id,
                    document_type="course",
                    content=course.description,
                    metadata={
                        "title": course.title,
                        "level": course.level,
                        "tags": course.tags
                    }
                )
            
            # Index chapters
            for chapter in chapters:
                await self.store_document_embedding(
                    document_id=str(chapter.id),
                    document_type="chapter",
                    content=chapter.content,
                    metadata={
                        "course_id": course_id,
                        "title": chapter.title,
                        "order": chapter.order
                    }
                )
            
            return True
        except Exception as e:
            raise Exception(f"Failed to index course content: {str(e)}")
    
    async def index_upload_content(self, upload_id: str) -> bool:
        """Index uploaded file content for vector search."""
        try:
            upload = await Upload.get(upload_id)
            if not upload or not upload.extracted_text:
                return False
            
            await self.store_document_embedding(
                document_id=upload_id,
                document_type="upload",
                content=upload.extracted_text,
                metadata={
                    "filename": upload.filename,
                    "file_type": upload.file_type,
                    "user_id": str(upload.user_id)
                }
            )
            
            return True
        except Exception as e:
            raise Exception(f"Failed to index upload content: {str(e)}")
    
    async def get_relevant_context(
        self, 
        query: str, 
        course_id: Optional[str] = None,
        upload_id: Optional[str] = None,
        limit: int = 5
    ) -> str:
        """Get relevant context for a query."""
        try:
            document_type = None
            if course_id:
                document_type = "course"
            elif upload_id:
                document_type = "upload"
            
            results = await self.search_similar_documents(
                query=query,
                document_type=document_type,
                limit=limit
            )
            
            context_parts = []
            for result in results:
                context_parts.append(result["content"])
            
            return "\n\n".join(context_parts)
        except Exception as e:
            raise Exception(f"Failed to get relevant context: {str(e)}")


# Global instance
vector_service = VectorService()
