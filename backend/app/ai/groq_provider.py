from app.ai.base import BaseAIProvider, AIResponse
from app.configuration import settings, logger


class GroqProvider(BaseAIProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else settings.GROQ_API_KEY
        self._client = None

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def default_model(self) -> str:
        return "llama-3.3-70b-versatile"

    def _get_client(self):
        if not self._client:
            from groq import AsyncGroq
            if not self.api_key or not self.api_key.strip():
                raise ValueError(
                    "GROQ_API_KEY is not configured in backend environment (.env). "
                    "Please set GROQ_API_KEY in backend/.env to use the Groq provider."
                )
            self._client = AsyncGroq(api_key=self.api_key.strip())
        return self._client

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.8,
        max_tokens: int = 1500,
        model: str | None = None
    ) -> AIResponse:
        client = self._get_client()
        initial_model = model or self.default_model
        candidate_models = [initial_model]
        
        # Fallback options in case rate limits (429) occur on the primary model
        fallbacks = ["llama-3.1-8b-instant", "qwen-2.5-32b", "deepseek-r1-distill-llama-70b"]
        for m in fallbacks:
            if m not in candidate_models:
                candidate_models.append(m)

        last_error = None
        for current_model in candidate_models:
            logger.info(f"GroqProvider calling Groq API: model={current_model}, temp={temperature}")
            logger.info(f"PROMPT SENT TO AI:\n{user_prompt[:250]}...")

            try:
                response = await client.chat.completions.create(
                    model=current_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                content = response.choices[0].message.content.strip()
                logger.info(f"AI RESPONSE RECEIVED with model={current_model} (length={len(content)} chars):\n{content[:150]}...")

                return AIResponse(
                    content=content,
                    provider=self.provider_name,
                    model=current_model
                )
            except Exception as e:
                logger.warning(f"Groq API call with model '{current_model}' failed: {str(e)}")
                last_error = e

        logger.error(f"All Groq fallback models failed. Last error: {str(last_error)}")
        raise RuntimeError(f"Groq AI provider error: {str(last_error)}")
