"""Upload model."""

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.base import PyObjectId


class UploadStatus(str, Enum):
    """Upload processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FileType(str, Enum):
    """Supported file types."""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    VIDEO = "video"
    IMAGE = "image"


class Upload(Document):
    """Upload document model."""
    
    user_id: PyObjectId = Field(..., index=True)
    filename: str
    file_type: FileType
    file_path: str
    file_size: int
    status: UploadStatus = UploadStatus.PENDING
    extracted_text: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "uploads"
        indexes = [
            "user_id",
            "file_type",
            "status",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Upload(filename={self.filename}, user_id={self.user_id}, status={self.status})"
