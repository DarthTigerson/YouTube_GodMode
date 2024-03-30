from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
from starlette.responses import Response

from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_youtube(mocker):
    # Mock the YouTube class
    mock = mocker.patch('app.routers.youtube.YouTube')
    mock.return_value.streams.filter.return_value.first.return_value.download.return_value = "/fakepath/video.mp3"
    return mock

@pytest.fixture
def mock_subprocess(mocker):
    # Mock subprocess.run
    mock = mocker.patch('app.routers.youtube.subprocess.run')
    mock.return_value = MagicMock(returncode=0)
    return mock

@pytest.fixture
def mock_os_remove(mocker):
    # Mock os.remove
    mock = mocker.patch('os.remove')
    return mock

@pytest.fixture
def mock_os_makedirs(mocker):
    # Mock os.makedirs
    mock = mocker.patch('os.makedirs')
    return mock

@pytest.fixture
def mock_file_response(mocker):
    # Mock FileResponse to return a simple Response object
    mock = mocker.patch('app.routers.youtube.FileResponse')
    mock.return_value = Response(content=b"Fake content", media_type='audio/mpeg')
    return mock

def test_to_mp3_endpoint(mock_youtube, mock_subprocess, mock_os_remove, mock_os_makedirs, mock_file_response):
    response = client.get("/youtube/to_mp3?youtube_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    # Check for the fake content bytes
    assert response.content == b"Fake content"
    
@pytest.fixture
def mock_file_response_mp4(mocker):
    # Mock FileResponse to return a simple Response object for mp4
    mock = mocker.patch('app.routers.youtube.FileResponse')
    mock.return_value = Response(content=b"Fake mp4 content", media_type='video/mp4')
    return mock

def test_to_mp4_endpoint(mock_youtube, mock_os_remove, mock_os_makedirs, mock_file_response_mp4):
    response = client.get("/youtube/to_mp4?youtube_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    # Check for the fake content bytes specific to mp4
    assert response.content == b"Fake mp4 content"