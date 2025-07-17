from typing import List, Dict, Any, Tuple
import io
from PIL import Image
import torch 
import numpy as np
import uuid

from backend.src.models.image import Tag, ImageAnalysisResponse
from backend.src.core.config import get_settings
# Import the dependency function that now returns only the CLIP model
from backend.src.core.dependencies import get_all_image_models_and_processors 

import logging

logger = logging.getLogger(__name__)

# Constants for configuration
MIN_OVERALL_CONFIDENCE_FOR_TAG = 0.001 

class ImageAnalysisService:
    """
    Service responsible for image analysis logic, using only the CLIP model for zero-shot classification.
    """
    def __init__(self):
        # Destructure only the CLIP model and processor
        self.clip_model, self.clip_processor = get_all_image_models_and_processors()
        
        self.settings = get_settings() 

        logger.info("ImageAnalysisService initialized with CLIP model.") 

    async def analyze_image(self, image_data: bytes, filename: str) -> ImageAnalysisResponse:
        """
        Analyzes an image using the CLIP model for zero-shot classification.

        Args:
            image_data (bytes): The binary image data.
            filename (str): The original filename of the image.

        Returns:
            ImageAnalysisResponse: Object containing tags and confidences, with source model.
        """
        logger.info(f"Starting CLIP zero-shot analysis for image: '{filename}'") 
        try:
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            
            # Candidate labels for the CLIP model. Expand or modify as needed.
            candidate_labels = [
                # General categories
                "a photo of a person", "a photo of a group of people", "a photo of a crowd",
                "a photo of an object", "a photo of a building", "a photo of a vehicle",
                "a photo of an animal", "a photo of nature", "a photo of food",
                "a photo of a landscape", "a photo of a city", "a photo of a street",
                "a photo of a house", "a photo of a tree", "a photo of a flower",
                "a photo of a book", "a photo of a computer", "a photo of a phone",
                "a photo of a sport", "a photo of a game", "a photo of a boat",
                "a photo of an airplane", "a photo of a bird", "a photo of a fish",
                "a photo of a plant", "a photo of a beach", "a photo of mountains",
                "a photo of a forest", "a photo of the sky", "a photo of the sea",
                "a photo of a laptop", "a photo of a smartphone", "a photo of a coffee cup",
                "a photo of a sunset", "a photo of a night scene", "a photo of a day scene",
                "a photo of snow", "a photo of rain", "a photo of a bridge", "a photo of a road",

                # People and celebrity categories
                "a photo of a man", "a photo of a woman", "a photo of a child",
                "a photo of a baby", "a photo of an adult", "a photo of an elderly person",
                "a photo of a celebrity", "a photo of a famous person",
                "a photo of a musician", "a photo of a singer", "a photo of a dancer",
                "a photo of an actor", "a photo of an athlete", "a photo of a politician",
                "a photo of Michael Jackson", 
                "a photo of a pop star", "a photo of a rock star", "a photo of a legend",

                # Show/music contexts
                "a photo of a stage", "a photo of a concert", "a photo of a performance",
                "a photo of a microphone", "a photo of a musical instrument", "a photo of a guitar",
                "a photo of a piano", "a photo of a drum", "a photo of a band",
                "a photo of a concert hall", "a photo of an audience", "a photo of a spotlight",
                "a photo of an event", "a photo of a crowd cheering", "a photo of a live show",
                "a photo of a music festival", "a photo of a dance performance",

                # Other relevant categories
                "a photo of clothing", "a photo of a suit", "a photo of a jacket",
                "a photo of a hat", "a photo of shoes", "a photo of jewelry",
                "a photo of a smile", "a photo of an expressive face", "a photo of happiness",
                "a photo of a joyful moment", "a photo of a serious expression",
                "a photo of an art piece", "a photo of a painting", "a photo of a sculpture",
                "a photo of a drawing", "a photo of a graphic design",

                # For dogs
                "a photo of a dog", "a photo of a puppy", "a photo of a canine",
                "a photo of a pet", "a photo of a domestic animal", "a photo of a mammal",
                "a photo of a golden retriever", "a photo of a labrador", "a photo of a poodle",
                "a photo of a German shepherd", "a photo of a bulldog", "a photo of a beagle",
                "a photo of a chihuahua", "a photo of a husky", "a photo of a border collie",
                "a photo of a shiba inu", "a photo of a corgi", "a photo of a pug",
                "a photo of a terrier", "a photo of a mixed breed dog"
            ]

            inputs = self.clip_processor(text=candidate_labels, images=image, return_tensors="pt", padding=True)
            inputs = {k: v.to('cpu') for k, v in inputs.items()} 
            
            with torch.no_grad():
                outputs = self.clip_model(**inputs) 
            
            logits_per_image = outputs.logits_per_image
            probabilities = torch.softmax(logits_per_image, dim=1)[0]
            
            all_tags: List[Tag] = []
            for i, prob in enumerate(probabilities):
                tag_name = candidate_labels[i]
                confidence = prob.item() 
                if confidence >= self.settings.MIN_OVERALL_CONFIDENCE_FOR_TAG: 
                    all_tags.append(Tag(name=tag_name, confidence=confidence, source_model="CLIP Zero-Shot"))
        
            all_tags.sort(key=lambda t: t.confidence, reverse=True)

            # Simplify tag selection for CLIP only
            final_tags = self._select_top_n_tags(all_tags, 5)

            if not final_tags:
                logger.warning("No relevant tags found by the CLIP model. Returning 'unknown_object'.")
                final_tags.append(Tag(name="unknown_object", confidence=0.01, source_model="fallback"))


            cleaned_tags: List[Tag] = []
            for tag in final_tags:
                cleaned_name = tag.name.replace("a photo of a ", "").replace("a photo of an ", "").replace("a photo of ", "").strip()
                cleaned_tags.append(Tag(name=cleaned_name, confidence=tag.confidence, source_model=tag.source_model))


            logger.info(f"Analysis of '{filename}' completed. Final tags: {[f'{t.name} ({t.confidence:.2f} from {t.source_model})' for t in cleaned_tags]}")
            return ImageAnalysisResponse(
                image_id=str(uuid.uuid4()), 
                filename=filename,
                tags=cleaned_tags, 
                message="Image analysis completed with AI (CLIP Zero-Shot)." 
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
