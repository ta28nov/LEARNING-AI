"""File upload endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List
from app.schemas.upload import UploadResponse, UploadCreate
from app.models.upload import Upload, UploadStatus
from app.models.user import User
from app.auth import get_current_active_user
from app.services.file_service import file_service
from app.services.genai_service import genai_service
from app.services.vector_service import vector_service
from bson import ObjectId

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file."""
    try:
        # Save file
        file_info = await file_service.save_upload_file(file, str(current_user.id))
        
        # Create upload record
        upload = Upload(
            user_id=current_user.id,
            filename=file_info["filename"],
            file_type=file_info["file_type"],
            file_path=file_info["file_path"],
            file_size=file_info["file_size"],
            status=UploadStatus.PENDING
        )
        
        await upload.insert()
        
        # Process file in background (extract text)
        try:
            extracted_text = await file_service.extract_text_from_file(
                file_info["file_path"], file_info["file_type"]
            )
            
            # Clean and process text using AI
            cleaned_text = await genai_service.extract_text_from_content(extracted_text)
            
            # Update upload record
            upload.extracted_text = cleaned_text
            upload.status = UploadStatus.COMPLETED
            await upload.save()
            
            # Index content for vector search
            await vector_service.index_upload_content(str(upload.id))
            
        except Exception as e:
            upload.status = UploadStatus.FAILED
            upload.metadata = {"error": str(e)}
            await upload.save()
        
        return UploadResponse.model_validate(upload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/", response_model=List[UploadResponse])
async def get_uploads(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's uploaded files."""
    uploads = await Upload.find(
        Upload.user_id == current_user.id
    ).skip(skip).limit(limit).sort("-created_at").to_list()
    
    return [UploadResponse.model_validate(upload) for upload in uploads]


@router.get("/{upload_id}", response_model=UploadResponse)
async def get_upload(
    upload_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific upload."""
    try:
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this upload"
            )
        
        return UploadResponse.model_validate(upload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )


@router.delete("/{upload_id}")
async def delete_upload(
    upload_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete an upload."""
    try:
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this upload"
            )
        
        # Delete file from filesystem
        await file_service.delete_file(upload.file_path)
        
        # Delete upload record
        await upload.delete()
        
        return {"message": "Upload deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )


@router.get("/{upload_id}/status")
async def get_upload_status(
    upload_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get upload processing status."""
    try:
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this upload"
            )
        
        return {
            "id": str(upload.id),
            "status": upload.status,
            "processed_chunks": 1 if upload.extracted_text else 0
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )


@router.post("/{upload_id}/reprocess")
async def reprocess_upload(
    upload_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Reprocess an uploaded file."""
    try:
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to reprocess this upload"
            )
        
        # Reset status
        upload.status = UploadStatus.PROCESSING
        await upload.save()
        
        try:
            # Extract text again
            extracted_text = await file_service.extract_text_from_file(
                upload.file_path, upload.file_type
            )
            
            # Clean and process text using AI
            cleaned_text = await genai_service.extract_text_from_content(extracted_text)
            
            # Update upload record
            upload.extracted_text = cleaned_text
            upload.status = UploadStatus.COMPLETED
            upload.metadata = None  # Clear any previous errors
            await upload.save()
            
            # Re-index content for vector search
            await vector_service.index_upload_content(str(upload.id))
            
            return {"message": "Upload reprocessed successfully"}
        except Exception as e:
            upload.status = UploadStatus.FAILED
            upload.metadata = {"error": str(e)}
            await upload.save()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reprocess upload: {str(e)}"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
