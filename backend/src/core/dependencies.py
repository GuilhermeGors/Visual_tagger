from functools import lru_cache
import logging
from transformers import AutoProcessor, CLIPModel 
import torch

logger = logging.getLogger(__name__)

# CLIP model name for zero-shot classification
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"             

@lru_cache()
def get_all_image_models_and_processors(): # Function name kept for compatibility
    """
    Loads the CLIP model and its processor.
    Loaded only once due to lru_cache.
    """
    logger.info("Starting to load CLIP AI model...") 
    
    clip_model = None
    clip_processor = None

    try:
        logger.info(f"Loading CLIP model: {CLIP_MODEL_NAME}...")
        clip_processor = AutoProcessor.from_pretrained(CLIP_MODEL_NAME)
        # Load with torch.float16 (quantization)
        clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME, torch_dtype=torch.float16)
        clip_model.to('cpu')
        clip_model.eval()
        logger.info("CLIP model and processor loaded successfully and quantized to float16.")
        
        logger.info("CLIP AI model and processor loaded and ready for use.") 
        # Returns only the CLIP model and processor
        return clip_model, clip_processor
    except Exception as e:
        logger.error(f"Error loading CLIP AI model or processor: {e}", exc_info=True) 
        raise RuntimeError(f"Failed to load CLIP AI model: {e}")
