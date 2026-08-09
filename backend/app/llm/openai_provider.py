import asyncio
from app.llm.base import LLMProvider, LLMResponse
from app.config import settings


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self._client = None

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return "gpt-4o-mini"

    def _get_client(self):
        if not self._client:
            from openai import AsyncOpenAI
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY is not configured in .env")
            self._client = AsyncOpenAI(api_key=self.api_key)
        return self._client

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        model: str | None = None
    ) -> LLMResponse:
        client = self._get_client()
        used_model = model or self.default_model

        response = await client.chat.completions.create(
            model=used_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        content = response.choices[0].message.content.strip()
        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=used_model
        )
