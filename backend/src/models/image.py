from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class Tag(BaseModel):
    """
    Represents a single image analysis tag.
    """
    name: str = Field(..., description="The tag name (e.g., 'cat', 'building').")
    confidence: float = Field(..., ge=0.0, le=1.0, description="The tag confidence level, from 0.0 to 1.0.")
    source_model: str = Field("unknown", description="The AI model that generated this tag.")

class ImageAnalysisRequest(BaseModel):
    """
    Model for the image analysis request.
    Currently, we accept file upload. In the future, a URL may be added.
    """
    class Config:
        json_schema_extra = {
            "example": {
                # "file": "binary_image_data",  # Example of file field
            }
        }

class ImageAnalysisResponse(BaseModel):
    """
    Model for the image analysis response.
    Contains a list of tags and an identifier for the image (if applicable).
    """
    image_id: Optional[str] = Field(None, description="Unique ID for the analyzed image (if persisted).")
    filename: Optional[str] = Field(None, description="Original image file name.")
    tags: List[Tag] = Field(..., min_length=1, description="List of tags identified in the image with their respective confidence levels.")
    message: str = Field("Analysis completed successfully.", description="Analysis status message.")

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "a1b2c3d4e5f6",
                "filename": "my_image.jpg",
                "tags": [
                    {"name": "cat", "confidence": 0.98, "source_model": "General Classifier"},
                    {"name": "animal", "confidence": 0.95, "source_model": "General Classifier"},
                    {"name": "domestic", "confidence": 0.85, "source_model": "CLIP Zero-Shot"}
                ],
                "message": "Analysis completed successfully."
            }
        }
