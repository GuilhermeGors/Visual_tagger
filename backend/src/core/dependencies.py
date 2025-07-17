from functools import lru_cache
import logging
from transformers import AutoModelForImageClassification, AutoImageProcessor, AutoProcessor, CLIPModel 
import torch

logger = logging.getLogger(__name__)

GENERAL_CLASSIFIER_MODEL_NAME = "google/vit-base-patch16-224"
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

@lru_cache()
def get_all_image_models_and_processors():
    """
    Loads the general classification model and its processor,
    and the CLIP model and its processor.
    All are loaded only once due to lru_cache.
    """
    logger.info("Starting to load all AI models...")
    
    general_model = None
    general_processor = None
    clip_model = None
    clip_processor = None

    try:
        # --- General Classifier (ViT) Loading ---
        logger.info(f"Loading general classifier: {GENERAL_CLASSIFIER_MODEL_NAME}...")
        general_processor = AutoImageProcessor.from_pretrained(GENERAL_CLASSIFIER_MODEL_NAME)
        # Load with torch.float16 (quantization)
        general_model = AutoModelForImageClassification.from_pretrained(GENERAL_CLASSIFIER_MODEL_NAME, torch_dtype=torch.float16)
        general_model.to('cpu')
        general_model.eval()
        logger.info("General classifier and processor loaded successfully and quantized to float16.")

        # --- CLIP Model Loading ---
        logger.info(f"Loading CLIP model: {CLIP_MODEL_NAME}...")
        clip_processor = AutoProcessor.from_pretrained(CLIP_MODEL_NAME)
        # Load with torch.float16 (quantization)
        clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME, torch_dtype=torch.float16)
        clip_model.to('cpu')
        clip_model.eval()
        logger.info("CLIP model and processor loaded successfully and quantized to float16.")
        
        logger.info("All AI models and processors loaded and ready for use.")
        return general_model, general_processor, clip_model, clip_processor
    except Exception as e:
        logger.error(f"Error loading one or more AI models or processors: {e}", exc_info=True)
        raise RuntimeError(f"Failed to load AI models: {e}")
