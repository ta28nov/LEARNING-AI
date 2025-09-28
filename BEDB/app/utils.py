"""Utility functions for the application."""

from bson import ObjectId
from typing import Union, Optional
from fastapi import HTTPException, status


def validate_object_id(id_str: str, field_name: str = "ID") -> ObjectId:
    """Validate and convert string to ObjectId."""
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format"
        )


def safe_object_id_conversion(id_value: Union[str, ObjectId, None]) -> Optional[ObjectId]:
    """Safely convert string or ObjectId to ObjectId."""
    if id_value is None:
        return None
    
    if isinstance(id_value, ObjectId):
        return id_value
    
    if isinstance(id_value, str):
        try:
            return ObjectId(id_value)
        except Exception:
            return None
    
    return None


def object_id_to_str(obj_id: Union[ObjectId, str, None]) -> Optional[str]:
    """Convert ObjectId to string safely."""
    if obj_id is None:
        return None
    
    if isinstance(obj_id, ObjectId):
        return str(obj_id)
    
    if isinstance(obj_id, str):
        return obj_id
    
    return None
