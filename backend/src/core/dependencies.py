from functools import lru_cache
import logging
# Import classes for both model types
from transformers import AutoModelForImageClassification, AutoImageProcessor, AutoProcessor, CLIPModel 
import torch

logger = logging.getLogger(__name__)

## --- MODEL NAMES ---
GENERAL_CLASSIFIER_MODEL_NAME = "google/vit-base-patch16-224" # Model for general object classification
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"             # CLIP model for zero-shot classification

@lru_cache()
def get_all_image_models_and_processors():
    """
    Loads the general classification model and its processor,
    e o modelo CLIP e seu processador.
    All are loaded only once due to lru_cache.
    """
    logger.info("Iniciando o carregamento de todos os modelos de IA...")
    
    general_model = None
    general_processor = None
    clip_model = None
    clip_processor = None

    try:
        # --- Load General Classifier (ViT) ---
        logger.info(f"Carregando classificador geral: {GENERAL_CLASSIFIER_MODEL_NAME}...")
        general_processor = AutoImageProcessor.from_pretrained(GENERAL_CLASSIFIER_MODEL_NAME)
        general_model = AutoModelForImageClassification.from_pretrained(GENERAL_CLASSIFIER_MODEL_NAME)
        general_model.to('cpu')
        general_model.eval()
        logger.info("Classificador geral e processador carregados com sucesso.")

        # --- Load CLIP Model ---
        logger.info(f"Carregando modelo CLIP: {CLIP_MODEL_NAME}...")
        clip_processor = AutoProcessor.from_pretrained(CLIP_MODEL_NAME)
        clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        clip_model.to('cpu')
        clip_model.eval()
        logger.info("Modelo CLIP e processador carregados com sucesso.")
        
        logger.info("Todos os modelos de IA e processadores carregados e prontos para uso.")
        # Return all loaded components
        return general_model, general_processor, clip_model, clip_processor
    except Exception as e:
        logger.error(f"Erro ao carregar um ou mais modelos de IA ou processadores: {e}", exc_info=True)
        raise RuntimeError(f"Falha ao carregar modelos de IA: {e}")

# For debugging purposes (optional, can be removed in production)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print("--- Multiple AI Models Loading Test ---")
    
    try:
        general_m, general_p, clip_m, clip_p = get_all_image_models_and_processors()
        print(f"Classificador Geral carregado: {general_m.__class__.__name__}")
        print(f"Processador Geral carregado: {general_p.__class__.__name__}")
        print(f"Modelo CLIP carregado: {clip_m.__class__.__name__}")
        print(f"Processador CLIP carregado: {clip_p.__class__.__name__}")
        print("--- Test Completed ---")
    except RuntimeError as e:
        print(f"Erro durante o teste de carregamento: {e}")
