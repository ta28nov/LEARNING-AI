"""File processing service."""

import os
import aiofiles
import magic
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
from app.config import settings
from app.models.upload import FileType, UploadStatus
import PyPDF2
import docx
from io import BytesIO


class FileService:
    """Service for file processing and management."""
    
    def __init__(self):
        """Initialize file service."""
        self.upload_dir = settings.upload_dir
        self.max_file_size = settings.max_file_size
        self._ensure_upload_dir()
    
    def _ensure_upload_dir(self):
        """Ensure upload directory exists."""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_upload_file(self, file: UploadFile, user_id: str) -> Dict[str, Any]:
        """Save uploaded file and return file info."""
        # Validate file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {self.max_file_size} bytes"
            )
        
        # Determine file type
        file_type = self._get_file_type(file.filename)
        if not file_type:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )
        
        # Generate unique filename
        import uuid
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Save file
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save file: {str(e)}"
            )
        
        return {
            "filename": file.filename,
            "file_type": file_type,
            "file_path": file_path,
            "file_size": len(content),
            "file_id": file_id
        }
    
    def _get_file_type(self, filename: str) -> Optional[FileType]:
        """Determine file type from filename."""
        if not filename:
            return None
        
        extension = os.path.splitext(filename)[1].lower()
        
        if extension == '.pdf':
            return FileType.PDF
        elif extension in ['.doc', '.docx']:
            return FileType.DOCX
        elif extension == '.txt':
            return FileType.TXT
        elif extension in ['.mp4', '.avi', '.mov', '.wmv']:
            return FileType.VIDEO
        elif extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return FileType.IMAGE
        else:
            return None
    
    async def extract_text_from_file(self, file_path: str, file_type: FileType) -> str:
        """Extract text content from uploaded file."""
        try:
            if file_type == FileType.PDF:
                return await self._extract_pdf_text(file_path)
            elif file_type == FileType.DOCX:
                return await self._extract_docx_text(file_path)
            elif file_type == FileType.TXT:
                return await self._extract_txt_text(file_path)
            else:
                return ""
        except Exception as e:
            raise Exception(f"Failed to extract text from file: {str(e)}")
    
    async def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
            
            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract PDF text: {str(e)}")
    
    async def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract DOCX text: {str(e)}")
    
    async def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            raise Exception(f"Failed to extract TXT text: {str(e)}")
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from the filesystem."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information."""
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "exists": True
            }
        except FileNotFoundError:
            return {"exists": False}
        except Exception as e:
            raise Exception(f"Failed to get file info: {str(e)}")


# Global instance
file_service = FileService()
