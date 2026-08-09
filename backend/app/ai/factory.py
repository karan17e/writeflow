from app.ai.base import BaseAIProvider
from app.ai.mock_provider import MockAIProvider
from app.ai.groq_provider import GroqProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.gemini_provider import GeminiProvider
from app.configuration import settings, logger


def get_ai_provider(provider_name: str | None = None) -> BaseAIProvider:
    name = (provider_name or settings.LLM_PROVIDER).lower()

    if name == "groq":
        return GroqProvider()
    elif name == "openai":
        return OpenAIProvider()
    elif name == "gemini":
        return GeminiProvider()
    elif name == "mock":
        return MockAIProvider()
    else:
        logger.warning(f"Unknown provider '{name}', falling back to MockAIProvider")
        return MockAIProvider()
