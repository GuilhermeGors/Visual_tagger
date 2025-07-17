import pytest
from pydantic import ValidationError
from typing import List

from backend.src.models.image import Tag, ImageAnalysisResponse

def test_tag_creation_valid():
    """
    Testa a criação de uma Tag com valores válidos.
    """
    tag = Tag(name="cat", confidence=0.95)
    assert tag.name == "cat"
    assert tag.confidence == 0.95

def test_tag_creation_min_confidence():
    """
    Testa se a confiança mínima de 0.0 é aceita.
    """
    tag = Tag(name="sky", confidence=0.0)
    assert tag.confidence == 0.0

def test_tag_creation_max_confidence():
    """
    Testa se a confiança máxima de 1.0 é aceita.
    """
    tag = Tag(name="tree", confidence=1.0)
    assert tag.confidence == 1.0

def test_tag_creation_invalid_confidence_low():
    """
    Testa se a criação de uma Tag falha com confiança abaixo de 0.0.
    """
    with pytest.raises(ValidationError):
        Tag(name="invalid", confidence=-0.1)

def test_tag_creation_invalid_confidence_high():
    """
    Testa se a criação de uma Tag falha com confiança acima de 1.0.
    """
    with pytest.raises(ValidationError):
        Tag(name="invalid", confidence=1.1)

def test_tag_creation_missing_name():
    """
    Testa se a criação de uma Tag falha sem o campo 'name'.
    """
    with pytest.raises(ValidationError):
        Tag(confidence=0.5) # type: ignore

def test_image_analysis_response_valid():
    """
    Testa a criação de uma ImageAnalysisResponse válida.
    """
    tags = [
        Tag(name="car", confidence=0.99),
        Tag(name="road", confidence=0.8)
    ]
    response = ImageAnalysisResponse(
        image_id="abc123def456",
        filename="test.jpg",
        tags=tags,
        message="Análise ok."
    )
    assert response.image_id == "abc123def456"
    assert response.filename == "test.jpg"
    assert len(response.tags) == 2
    assert response.tags[0].name == "car"
    assert response.message == "Análise ok."

def test_image_analysis_response_no_filename_and_id():
    """
    Testa a criação de uma ImageAnalysisResponse sem filename e image_id (opcionais).
    """
    tags = [Tag(name="water", confidence=0.7)]
    response = ImageAnalysisResponse(tags=tags)
    assert response.image_id is None
    assert response.filename is None
    assert len(response.tags) == 1
    assert response.message == "Análise concluída com sucesso." # Mensagem padrão

def test_image_analysis_response_empty_tags():
    """
    Testa a criação de uma ImageAnalysisResponse com lista de tags vazia.
    """
    with pytest.raises(ValidationError):
        # A lista de tags é Required Field, então não pode ser vazia ou None sem o padrão
        # Se você permitir tags vazias, mude a assinatura em models/image.py: tags: List[Tag] = Field(default_factory=list, ...)
        ImageAnalysisResponse(filename="empty.png", tags=[]) # type: ignore

def test_image_analysis_response_missing_tags():
    """
    Testa se a criação de uma ImageAnalysisResponse falha sem o campo 'tags'.
    """
    with pytest.raises(ValidationError):
        ImageAnalysisResponse(filename="no_tags.png") # type: ignore