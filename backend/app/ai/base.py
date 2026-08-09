from abc import ABC, abstractmethod


class AIResponse:
    def __init__(self, content: str, provider: str, model: str):
        self.content = content
        self.provider = provider
        self.model = model


class BaseAIProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        pass

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        model: str | None = None
    ) -> AIResponse:
        pass
