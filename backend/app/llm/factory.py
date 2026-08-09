from app.llm.base import LLMProvider
from app.llm.mock_provider import MockProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.gemini_provider import GeminiProvider
from app.config import settings


def get_provider(provider_name: str | None = None) -> LLMProvider:
    name = (provider_name or settings.LLM_PROVIDER).lower()

    if name == "openai":
        return OpenAIProvider()
    elif name == "gemini":
        return GeminiProvider()
    elif name == "mock":
        return MockProvider()
    else:
        # Fallback to MockProvider if unknown or missing key
        return MockProvider()
