import pytest
from unittest.mock import AsyncMock, patch
import os
import io

from backend.src.services.image_analysis import ImageAnalysisService
from backend.src.models.image import Tag, ImageAnalysisResponse

## === ATTENTION: ADJUST THESE TWO VALUES ===
# Put the EXACT name of image file here
TEST_IMAGE_FILENAME = "dog.jpg" # EX: "my_dog.png" or "dog.jpg"
TEST_IMAGE_PATH = os.path.join("backend", "tests", "assets", TEST_IMAGE_FILENAME)


@pytest.mark.asyncio
async def test_image_analysis_service_mock_behavior():
    """
    Tests if the image analysis service returns a simulated response,
    reading a real image from disk.
    """
    # Load the image data from file
    mock_image_data = None
    try:
        with open(TEST_IMAGE_PATH, "rb") as f:
            mock_image_data = f.read()
    except FileNotFoundError:
        # If the file is not found, the test fails explicitly
        pytest.fail(f"Test image file not found: {TEST_IMAGE_PATH}. "
                    f"Make sure the image '{TEST_IMAGE_FILENAME}' is in the 'backend/tests/assets/' folder.")

    # Mock random.sample, random.uniform, and get_settings
    with patch('backend.src.services.image_analysis.get_settings') as mock_get_settings, \
         patch('random.sample', return_value=['mock_tag1', 'mock_tag2']), \
         patch('random.uniform', return_value=0.85):

        mock_settings_instance = mock_get_settings.return_value
        mock_settings_instance.AI_MODEL_CONFIDENCE_THRESHOLD = 0.5 # Ensures that 0.85 passes the filter

        service = ImageAnalysisService() # The service instance will be created AFTER the get_settings mock

        # Make sure the image data was loaded before calling the service
        assert mock_image_data is not None, "mock_image_data should not be None here."

        response = await service.analyze_image(mock_image_data, TEST_IMAGE_FILENAME) # Pass the exact file name

        assert isinstance(response, ImageAnalysisResponse)
        assert response.filename == TEST_IMAGE_FILENAME # Assert with the exact file name
        assert len(response.tags) > 0
        assert response.tags[0].name in ['mock_tag1', 'mock_tag2']
        assert response.tags[0].confidence == pytest.approx(0.85)
        assert "Análise simulada" in response.message
        # Adicione asserções para garantir que NÃO são tags de erro
        assert "invalid_image_format" not in [tag.name for tag in response.tags]
        assert "Formato de imagem inválido" not in response.message