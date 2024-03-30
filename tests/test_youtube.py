from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
from starlette.responses import Response  # Make sure to import Response

from app.main import app  # Ensure this is the correct import path

client = TestClient(app)

@pytest.fixture
def mock_youtube(mocker):
    mock = mocker.patch('pytube.YouTube')
    mock.return_value.streams.filter.return_value.first.return_value.download.return_value = "video.mp3"
    return mock

@pytest.fixture
def mock_subprocess(mocker):
    mock = mocker.patch('subprocess.run')
    mock.return_value = MagicMock(returncode=0)
    return mock

@pytest.fixture
def mock_os_remove(mocker):
    mock = mocker.patch('os.remove')
    return mock

@pytest.fixture
def mock_os_makedirs(mocker):
    mock = mocker.patch('os.makedirs')
    return mock

@pytest.fixture
def mock_file_response(mocker):
    # Now that Response is imported, this should work correctly
    mock = mocker.patch('fastapi.responses.FileResponse', return_value=Response(content=b'', media_type='audio/mpeg'))
    return mock

def test_to_mp3_endpoint(mock_youtube, mock_subprocess, mock_os_remove, mock_os_makedirs, mock_file_response):
    response = client.get("/youtube/to_mp3?youtube_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    # Here you can add more assertions if necessary

def test_to_mp4_endpoint(mock_youtube, mock_os_remove, mock_os_makedirs, mock_file_response):
    response = client.get("/youtube/to_mp4?youtube_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    # Here you can add more assertions if necessary
