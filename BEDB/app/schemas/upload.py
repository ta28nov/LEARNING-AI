"""Upload related schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.upload import FileType, UploadStatus


class UploadCreate(BaseModel):
    """Upload creation schema."""
    filename: str
    file_type: FileType
    file_size: int


class UploadResponse(BaseModel):
    """Upload response schema."""
    id: str
    user_id: str
    filename: str
    file_type: FileType
    file_path: str
    file_size: int
    status: UploadStatus
    extracted_text: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UploadUpdate(BaseModel):
    """Upload update schema."""
    extracted_text: Optional[str] = None
    metadata: Optional[dict] = None
