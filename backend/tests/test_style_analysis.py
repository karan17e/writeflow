import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.prompts import PromptBuilder
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


def test_anti_copying_guardrails_in_system_prompt():
    system_prompt = PromptBuilder.get_system_prompt()
    assert "DO NOT COPY SENTENCES OR REPRODUCE UNIQUE PHRASES DIRECTLY FROM USER WRITING SAMPLES" in system_prompt


@pytest.mark.asyncio
async def test_analyze_style_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "samples": [
                "Here is my first writing sample. Short sentences. High impact.",
                "Second sample. Always focus on practical execution over theory."
            ],
            "provider": "mock"
        }
        response = await ac.post("/api/analyze-style", json=payload)
    
    assert response.status_code == 200
    profile = response.json()
    assert "formality" in profile
    assert "sentence_length" in profile
    assert "vocabulary" in profile
    assert "emoji_usage" in profile


@pytest.mark.asyncio
async def test_generate_post_with_writing_samples():
    req = GenerateRequest(
        topic="Building software fast",
        writing_samples=[
            "I write directly. No fluff. Short lines.",
            "Execution is everything. Start small and iterate."
        ],
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["has_style_profile"] is True
    assert "style_profile" in response.metadata
