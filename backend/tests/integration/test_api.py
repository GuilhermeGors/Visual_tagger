import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock 
import os

# The import of the main application must be ABSOLUTE from the project root perspective
from backend.src.main import app
# Import models directly to use with MagicMock
from backend.src.models.image import ImageAnalysisResponse, Tag 


# Define the path to the test image file
TEST_IMAGE_FILENAME = "dog.jpg" 
TEST_IMAGE_PATH = os.path.join("backend", "tests", "assets", TEST_IMAGE_FILENAME)

# Create a test client for the FastAPI application
client = TestClient(app)

# Fixture to load the test image only once
@pytest.fixture(scope="module")
def test_image_data():
    """Loads the binary data of the test image once for all tests."""
    try:
        with open(TEST_IMAGE_PATH, "rb") as f:
            return f.read()
    except FileNotFoundError:
        pytest.fail(f"Test image file not found: {TEST_IMAGE_PATH}. "
                    f"Make sure the image '{TEST_IMAGE_FILENAME}' is in the 'backend/tests/assets/' folder.")

# This ensures the mock affects the instance already created in analyze.py
@pytest.fixture(autouse=True) 
def mock_image_analysis_service_instance(): # Renamed back to 'instance'
    """
    Mocks the global 'image_analysis_service' instance in the analyze.py module.
    This ensures the mock affects the instance actually used by the endpoint.
    """
    # The patch path must be where the INSTANCE 'image_analysis_service' is REFERENCED in analyze.py
    with patch('backend.src.api.v1.endpoints.analyze.image_analysis_service') as mock_service_instance:
        # Ensures the analyze_image method of the mock is asynchronous
        mock_service_instance.analyze_image = AsyncMock() 
        yield mock_service_instance # Returns the mocked instance for the tests to use

# Integration test for the /api/v1/analyze endpoint
# The fixture name was fixed to 'mock_image_analysis_service_instance'
def test_analyze_image_endpoint_success(test_image_data, mock_image_analysis_service_instance): 
    """
    Tests if the POST /api/v1/analyze endpoint returns a successful response
    with simulated tags.
    """
    # Sets the return value of the mock's analyze_image method to be an ImageAnalysisResponse OBJECT
    mock_image_analysis_service_instance.analyze_image.return_value = ImageAnalysisResponse(
        image_id="mock_id_123", # This ID will be returned by the mock
        filename=TEST_IMAGE_FILENAME,
        tags=[
            Tag(name="mock_tag_integration_1", confidence=0.9),
            Tag(name="mock_tag_integration_2", confidence=0.8)
        ],
        message="Simulated integration analysis."
    )

    # Prepares the multipart/form-data file request
    files = {'file': (TEST_IMAGE_FILENAME, test_image_data, 'image/jpeg')} 

    # Makes the POST request to the endpoint
    response = client.post("/api/v1/analyze", files=files)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["image_id"] == "mock_id_123" # Now this assert should pass
    assert data["filename"] == TEST_IMAGE_FILENAME
    assert len(data["tags"]) == 2
    assert data["tags"][0]["name"] == "mock_tag_integration_1"
    assert data["tags"][1]["name"] == "mock_tag_integration_2"
    assert data["message"] == "Simulated integration analysis."
    
    # Checks if the analysis service was called with the correct arguments
    mock_image_analysis_service_instance.analyze_image.assert_called_once_with(test_image_data, TEST_IMAGE_FILENAME)

# The fixture name was fixed to 'mock_image_analysis_service_instance'
def test_analyze_image_endpoint_invalid_file_type(test_image_data, mock_image_analysis_service_instance): 
    """
    Tests if the POST /api/v1/analyze endpoint rejects invalid file types.
    """
    # Use a plain text file as an example of an invalid type
    invalid_file_data = b"This is not an image."
    invalid_filename = "test.txt"
    files = {'file': (invalid_filename, invalid_file_data, 'text/plain')}

    response = client.post("/api/v1/analyze", files=files)

    assert response.status_code == 400
    # More robust assertion for the detail message
    assert "invalid file type" in response.json()["detail"].lower()

    # The service should not be called in this case
    mock_image_analysis_service_instance.analyze_image.assert_not_called()


# The fixture name was fixed to 'mock_image_analysis_service_instance'
def test_analyze_image_endpoint_no_file(mock_image_analysis_service_instance): 
    """
    Tests if the POST /api/v1/analyze endpoint returns an error when no file is sent.
    """
    # The service should not be called in this case
    mock_image_analysis_service_instance.analyze_image.assert_not_called()

    response = client.post("/api/v1/analyze")

    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()

def test_analyze_image_endpoint_service_exception(test_image_data, mock_image_analysis_service_instance): 
    """
    Tests how the endpoint handles exceptions in the analysis service.
    """
    # Sets the mock to raise an exception when calling analyze_image
    mock_image_analysis_service_instance.analyze_image.side_effect = Exception("Simulated AI model error")

    files = {'file': (TEST_IMAGE_FILENAME, test_image_data, 'image/jpeg')} 
    response = client.post("/api/v1/analyze", files=files)

    assert response.status_code == 500
    assert "an internal error occurred while processing the image." in response.json()["detail"].lower()
    assert "simulated ai model error" in response.json()["detail"].lower()

    mock_image_analysis_service_instance.analyze_image.assert_called_once()