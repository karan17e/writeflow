import asyncio
from app.ai.base import BaseAIProvider, AIResponse
from app.configuration import settings, logger


class GeminiProvider(BaseAIProvider):
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
    ) -> AIResponse:
        import google.generativeai as genai

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        genai.configure(api_key=self.api_key)
        used_model = model or self.default_model

        logger.info(f"GeminiProvider calling model={used_model}")
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        model_instance = genai.GenerativeModel(
            model_name=used_model,
            system_instruction=system_prompt,
            generation_config=generation_config
        )

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model_instance.generate_content(user_prompt)
        )

        content = response.text.strip()
        return AIResponse(
            content=content,
            provider=self.provider_name,
            model=used_model
        )
