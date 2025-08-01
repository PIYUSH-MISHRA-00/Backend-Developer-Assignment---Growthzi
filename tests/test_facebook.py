import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_facebook_ideas_missing_website(client):
    response = client.post('/api/facebook/ideas', json={})
    assert response.status_code == 400
    assert b"website_url is required" in response.data

def test_facebook_ideas_success(monkeypatch, client):
    def mock_generate_text(self, prompt):
        return json.dumps({
            "business_tips": ["Tip1", "Tip2", "Tip3"],
            "promotions": ["Promo1", "Promo2", "Promo3"],
            "industry_insights": ["Insight1", "Insight2", "Insight3"]
        })
    from app.services.gemini_service import GeminiService
    monkeypatch.setattr(GeminiService, 'generate_text', mock_generate_text)

    payload = {"website_url": "https://xyz.com", "industry": "ecommerce"}
    response = client.post('/api/facebook/ideas', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "business_tips" in data

def test_facebook_planner_missing_fields(client):
    response = client.post('/api/facebook/planner', json={})
    assert response.status_code == 400
    assert b"frequency, tone, and post_mix are required" in response.data

def test_facebook_planner_success(monkeypatch, client):
    def mock_generate_text(self, prompt):
        return json.dumps({
            "Monday": "Post about something",
            "Thursday": "Promo post"
        })
    from app.services.gemini_service import GeminiService
    monkeypatch.setattr(GeminiService, 'generate_text', mock_generate_text)

    payload = {"frequency": 2, "tone": "witty", "post_mix": ["educational", "promotional"]}
    response = client.post('/api/facebook/planner', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "Monday" in data

def test_facebook_posts_get_and_update(client):
    # Clear posts_store before test
    from app.routes.facebook import posts_store
    posts_store.clear()

    response = client.get('/api/facebook/posts')
    assert response.status_code == 200
    assert response.get_json() == []

def test_facebook_publish_missing_content(client):
    response = client.post('/api/facebook/publish', json={})
    assert response.status_code == 400
    assert b"Post content is required" in response.data
