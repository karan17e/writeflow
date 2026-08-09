import asyncio
import re
from app.ai.base import BaseAIProvider, AIResponse
from app.configuration import logger


class MockAIProvider(BaseAIProvider):
    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def default_model(self) -> str:
        return "mock-v1"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        model: str | None = None
    ) -> AIResponse:
        used_model = model or self.default_model
        logger.info(f"MockAIProvider generating content with model={used_model}, temp={temperature}")

        await asyncio.sleep(0.05)

        # Extract topic from user prompt if present
        topic_match = re.search(r"PRIMARY TOPIC.*?:?\s*(.*)", user_prompt, re.IGNORECASE)
        if not topic_match:
            topic_match = re.search(r"Topic.*?:?\s*(.*)", user_prompt, re.IGNORECASE)

        topic = topic_match.group(1).strip() if topic_match else "your topic"
        # Clean up any trailing labels
        topic = topic.splitlines()[0] if topic else "your requested topic"

        if "auditor" in system_prompt.lower() or "validate_relevance" in system_prompt.lower():
            content = '{"is_relevant": true, "relevance_score": 9, "has_invented_information": false, "has_unrelated_content": false, "is_template_repetitive": false, "issues": []}'
        elif "style profile" in system_prompt.lower() or "linguistic analyst" in system_prompt.lower():
            content = '{"formality": "casual-professional", "sentence_length": "short", "vocabulary": "simple", "paragraph_structure": "short-paragraphs", "emoji_usage": "low", "hook_style": "direct", "use_of_questions": "rare", "storytelling": "moderate"}'
        elif "quality" in system_prompt.lower() or "performance analyst" in system_prompt.lower():
            content = '{"hook_strength": 8, "clarity": 9, "specificity": 8, "readability": 9, "personal_voice": 8, "generic_language": 2, "buzzword_usage": 1, "repetition": 2, "emoji_usage": 9, "hashtag_quality": 8, "overall_score": 8, "suggestions": ["Strong direct hook", "Good readability"]}'
        else:
            content = (
                f"Reflecting on {topic} has been an insightful experience.\n\n"
                f"Working directly on {topic} taught me the value of hands-on practice over theory.\n\n"
                f"The key takeaway wasn't just completing the work, but understanding the core principles behind it.\n\n"
                f"Still learning every day."
            )

        return AIResponse(
            content=content,
            provider=self.provider_name,
            model=used_model
        )
