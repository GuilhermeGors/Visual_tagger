from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from typing import List
import io
import logging

from backend.src.models.image import ImageAnalysisResponse
# --- MUDANÇA: Importar o ImageAnalysisService para tipagem e a classe de dependência
from backend.src.services.image_analysis import ImageAnalysisService

logger = logging.getLogger(__name__)

router = APIRouter()

# --- NOVA FUNÇÃO DE DEPENDÊNCIA ---
# Esta função será usada pelo FastAPI para injetar a instância do serviço
def get_image_analysis_service_instance() -> ImageAnalysisService:
    """
    Retorna uma instância do ImageAnalysisService.
    FastAPI irá gerenciar o ciclo de vida desta dependência.
    """
    return ImageAnalysisService()

@router.post(
    "/analyze",
    response_model=ImageAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analisa uma imagem enviada e retorna tags e confianças.",
    description="Recebe uma imagem como arquivo (multipart/form-data), a processa usando o serviço de análise de IA e retorna uma lista de tags identificadas com seus respectivos níveis de confiança."
)
async def analyze_image_endpoint(
    file: UploadFile = File(..., description="O arquivo de imagem a ser analisado (JPEG, PNG)."),
    # --- MUDANÇA: Injetar a instância do serviço ---
    image_analysis_service: ImageAnalysisService = Depends(get_image_analysis_service_instance)
) -> ImageAnalysisResponse:
    """
    Endpoint para análise de imagem.
    Recebe um arquivo de imagem, envia para o serviço de análise de IA
    e retorna os resultados.
    """
    logger.info(f"Requisição POST /api/v1/analyze recebida para o arquivo: {file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning(f"Tipo de arquivo inválido recebido: {file.content_type} para {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo inválido. Por favor, envie uma imagem (ex: JPEG, PNG, JPEG)."
        )

    try:
        # Lê o conteúdo do arquivo
        image_data = await file.read()
        logger.info(f"Dados da imagem de {file.filename} lidos ({len(image_data)} bytes).")

        # Chama o serviço de análise de imagem injetado
        response = await image_analysis_service.analyze_image(image_data, file.filename)
        logger.info(f"Análise de {file.filename} concluída com sucesso.")

        return response
    except ValueError as ve: # Captura erros específicos do serviço, como formato de imagem
        logger.error(f"Erro de validação no serviço para {file.filename}: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except RuntimeError as re: # Captura erros internos do serviço (ex: falha do modelo)
        logger.error(f"Erro de runtime no serviço para {file.filename}: {re}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno no serviço de análise. Detalhe: {re}"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao processar imagem {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno desconhecido ao processar a imagem. Detalhe: {e}"
        )

