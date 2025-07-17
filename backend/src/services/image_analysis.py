from typing import List, Dict, Any, Tuple
import io
from PIL import Image
import random # For mock data
import uuid

from backend.src.models.image import Tag, ImageAnalysisResponse
from backend.src.core.config import get_settings
# REMOVIDO: from backend.src.core.dependencies import get_all_image_models_and_processors 

import logging

logger = logging.getLogger(__name__)

# Constants for configuration (still useful for mock logic)
MIN_OVERALL_CONFIDENCE_FOR_TAG = 0.001 

class ImageAnalysisService:
    """
    Service responsible for image analysis logic.
    For Vercel Free Tier deployment, actual AI inference is mocked due to size limits.
    """
    def __init__(self):
        # Models are not loaded here for Vercel Free Tier deployment
        # self.clip_model, self.clip_processor = get_all_image_models_and_processors() # REMOVIDO
        
        self.settings = get_settings() 

        logger.info("ImageAnalysisService initialized. Using mock AI inference for Vercel Free Tier.") 

    async def analyze_image(self, image_data: bytes, filename: str) -> ImageAnalysisResponse:
        """
        Analyzes an image using mock data.
        In a full deployment, this would involve actual AI model inference.

        Args:
            image_data (bytes): The binary image data.
            filename (str): The original filename of the image.

        Returns:
            ImageAnalysisResponse: Object containing tags and confidences, with source model.
        """
        logger.info(f"Starting mock analysis for image: '{filename}'") 
        try:
            # Basic image validation (still useful)
            Image.open(io.BytesIO(image_data))
            
            # --- MOCK INFERENCE LOGIC ---
            mock_tags_pool = [
                "person", "dog", "cat", "building", "food", "car", "nature", 
                "Michael Jackson", "concert", "city", "street", "tree", "flower",
                "laptop", "smartphone", "beach", "mountain", "forest", "sky", "water"
            ]

            num_tags = random.randint(3, 5) # Generate 3 to 5 tags
            selected_mock_tags = random.sample(mock_tags_pool, num_tags)

            all_tags: List[Tag] = []
            for tag_name in selected_mock_tags:
                confidence = round(random.uniform(0.1, 0.99), 2) # Random confidence
                all_tags.append(Tag(name=tag_name, confidence=confidence, source_model="Mock AI"))
            
            all_tags.sort(key=lambda t: t.confidence, reverse=True)

            # Ensure we return top 5, even if mock generates less
            final_tags = self._select_top_n_tags(all_tags, 5)

            if not final_tags:
                logger.warning("No relevant mock tags generated. Returning 'unknown_object'.")
                final_tags.append(Tag(name="unknown_object", confidence=0.01, source_model="fallback"))


            cleaned_tags: List[Tag] = []
            for tag in final_tags:
                # No "a photo of a" prefix to remove from mock tags
                cleaned_tags.append(Tag(name=tag.name, confidence=tag.confidence, source_model=tag.source_model))


            logger.info(f"Analysis of '{filename}' completed. Final tags: {[f'{t.name} ({t.confidence:.2f} from {t.source_model})' for t in cleaned_tags]}")
            return ImageAnalysisResponse(
                image_id=str(uuid.uuid4()), 
                filename=filename,
                tags=cleaned_tags, 
                message="Image analysis completed (Mock AI for Vercel Free Tier)." 
            )

        except Image.UnidentifiedImageError:
            logger.error(f"Error: Unidentified image format for '{filename}'.")
            raise ValueError("Invalid or corrupted image format.")
        except Exception as e:
            logger.error(f"Unexpected error during image analysis for '{filename}': {e}", exc_info=True)
            raise RuntimeError(f"Internal error in image analysis service: {e}")

    def _select_top_n_tags(self, all_tags: List[Tag], n: int) -> List[Tag]:
        """
        Selects the top N tags from an already sorted list.
        """
        return all_tags[:n]
