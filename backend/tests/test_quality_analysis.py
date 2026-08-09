import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_analyze_quality_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "post": "Stop making this basic mistake when launching products. Focus on real user feedback from day 1.",
            "provider": "mock"
        }
        response = await ac.post("/api/analyze", json=payload)
    
    assert response.status_code == 200
    scores = response.json()
    assert "hook_strength" in scores
    assert "clarity" in scores
    assert "specificity" in scores
    assert "readability" in scores
    assert "personal_voice" in scores
    assert "generic_language" in scores
    assert "buzzword_usage" in scores
    assert "repetition" in scores
    assert "emoji_usage" in scores
    assert "hashtag_quality" in scores
    assert "overall_score" in scores
    assert "suggestions" in scores
    assert isinstance(scores["suggestions"], list)
