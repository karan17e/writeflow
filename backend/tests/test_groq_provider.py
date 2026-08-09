import pytest
from app.ai.groq_provider import GroqProvider
from app.ai.factory import get_ai_provider
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


@pytest.mark.asyncio
async def test_groq_missing_api_key_error():
    # Instantiating GroqProvider with empty key should raise a clear ValueError when generating
    provider = GroqProvider(api_key="")
    with pytest.raises(ValueError) as exc_info:
        await provider.generate(system_prompt="Test", user_prompt="Test prompt")
    
    assert "GROQ_API_KEY is not configured" in str(exc_info.value)


@pytest.mark.asyncio
async def test_groq_provider_factory():
    provider = get_ai_provider("groq")
    assert isinstance(provider, GroqProvider)
    assert provider.provider_name == "groq"
    assert provider.default_model == "llama-3.3-70b-versatile"


@pytest.mark.asyncio
async def test_mock_provider_fallback_safe():
    # Verify fallback to mock provider works cleanly without exposing any keys
    req = GenerateRequest(
        topic="Testing Groq modular architecture",
        post_type="Story",
        tone="Conversational",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert "metadata" in response.model_dump()
    # Security assertion: ensure no API key fields exist in metadata
    metadata = response.metadata
    assert "api_key" not in metadata
    assert "groq_api_key" not in metadata
    assert "secret" not in metadata
