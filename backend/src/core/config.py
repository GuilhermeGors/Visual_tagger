from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.
    """
    """
    Application settings loaded from environment variables.
    """
    APP_NAME: str = "VisualTagger Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- NOVAS CONFIGURAÇÕES DE THRESHOLDS ---
    # --- NEW THRESHOLD SETTINGS ---
    MIN_OVERALL_CONFIDENCE_FOR_TAG: float = 0.001 # General threshold for tags
    HIGH_CONFIDENCE_THRESHOLD_GENERAL: float = 0.6 # Threshold for general classifier
    MIN_CONFIDENT_TAGS_GENERAL: int = 2 # Minimum confident tags from general classifier

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))


@lru_cache()
def get_settings():
    """
    Retorna uma única instância das configurações da aplicação.
    Usado para garantir que as configurações sejam carregadas apenas uma vez.
    """
    """
    Returns a single instance of the application settings.
    Used to ensure that the settings are loaded only once.
    """
    logger.info("Tentando obter configurações da aplicação...")
    settings = Settings()
    logger.info(f"Configurações obtidas: DEBUG={settings.DEBUG}, "
                f"MIN_OVERALL_CONFIDENCE_FOR_TAG={settings.MIN_OVERALL_CONFIDENCE_FOR_TAG}, "
                f"HIGH_CONFIDENCE_THRESHOLD_GENERAL={settings.HIGH_CONFIDENCE_THRESHOLD_GENERAL}, "
                f"MIN_CONFIDENT_TAGS_GENERAL={settings.MIN_CONFIDENT_TAGS_GENERAL}")
    return settings