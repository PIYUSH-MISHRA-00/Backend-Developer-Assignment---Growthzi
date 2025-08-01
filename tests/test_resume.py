import io
import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_parse_resume_no_file(client):
    response = client.post('/api/parse-resume')
    assert response.status_code == 400
    assert b"No file part in the request" in response.data

def test_parse_resume_empty_file(client):
    data = {'file': (io.BytesIO(b''), '')}
    response = client.post('/api/parse-resume', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No selected file" in response.data

def test_parse_resume_unsupported_file(client):
    data = {'file': (io.BytesIO(b'test'), 'test.txt')}
    response = client.post('/api/parse-resume', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"Unsupported file type" in response.data

# Note: For full integration test, a valid PDF or DOC file and mocking GeminiService would be needed.
