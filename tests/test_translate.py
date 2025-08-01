import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_translate_content_missing_json(client):
    # Send empty body with application/json header to trigger JSON parse error
    response = client.post('/api/translate-content', data='', headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    assert b"Invalid JSON input" in response.data

def test_translate_content_missing_fields(client):
    response = client.post('/api/translate-content', json={})
    assert response.status_code == 400
    assert b"Both 'content' and 'target_lang' are required" in response.data

def test_translate_content_success(monkeypatch, client):
    def mock_generate_text(self, prompt):
        return '{"about": "Je suis un développeur", "hero": {"name": "John", "bio": "Développeur créatif"}}'
    from app.services.gemini_service import GeminiService
    monkeypatch.setattr(GeminiService, 'generate_text', mock_generate_text)

    payload = {
        "content": {"about": "I am a developer", "hero": {"name": "John", "bio": "Creative Dev"}},
        "target_lang": "fr"
    }
    response = client.post('/api/translate-content', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data.get('about') == "Je suis un développeur"
