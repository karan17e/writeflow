import asyncio
from app.llm.base import LLMProvider, LLMResponse
from app.config import settings


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return "gemini-1.5-flash"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        model: str | None = None
    ) -> LLMResponse:
        import google.generativeai as genai

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured in .env")

        genai.configure(api_key=self.api_key)
        used_model = model or self.default_model

        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        model_instance = genai.GenerativeModel(
            model_name=used_model,
            system_instruction=system_prompt,
            generation_config=generation_config
        )

        # Gemini SDK generate_content is synchronous/blocking, run in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model_instance.generate_content(user_prompt)
        )

        content = response.text.strip()
        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=used_model
        )
