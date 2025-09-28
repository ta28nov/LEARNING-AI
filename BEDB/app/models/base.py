# base.py
from typing import Any
from datetime import datetime
from beanie import Document
from bson import ObjectId
from pydantic import Field
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> str:
            if ObjectId.is_valid(value):
                return str(value)
            raise ValueError("Invalid ObjectId")

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x) if isinstance(x, (ObjectId, str)) else None
            ),
        )

class BaseDocument(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "from_attributes": True
    }

    class Settings:
        use_state_management = True

    def to_json(self):
        """Convert document to JSON with proper ID handling."""
        data = self.model_dump(by_alias=True)
        data["id"] = str(data.pop("_id"))  # Convert _id to id string
        return data
