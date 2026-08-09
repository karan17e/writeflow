import asyncio
from app.llm.base import LLMProvider, LLMResponse


class MockProvider(LLMProvider):
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
    ) -> LLMResponse:
        # Simulate small API delay
        await asyncio.sleep(0.3)

        used_model = model or self.default_model

        # Extract topic if present in user prompt
        topic_str = "your idea"
        if "about:" in user_prompt.lower():
            lines = [line for line in user_prompt.splitlines() if "about:" in line.lower()]
            if lines:
                topic_str = lines[0].split(":", 1)[-1].strip()

        # Check if refinement directive
        if "REWRITE" in system_prompt or "REWRITE" in user_prompt:
            content = f"Here is a fresh take on {topic_str}.\n\nI used to think success was linear. Then I had a real wake-up call.\n\nKey takeaways:\n- Focus on what you control.\n- Iterate fast, learn faster.\n- Stay consistent even when it's hard.\n\nWhat's one lesson you learned the hard way this year?"
        elif "PERSONAL" in system_prompt or "PERSONAL" in user_prompt:
            content = f"I'll be honest with you about {topic_str}.\n\nLast month, I hit a massive wall. I thought we were doing everything right, but the numbers proved otherwise.\n\nHere is what I personally changed:\n1. Stopped guessing, started listening\n2. Scaled back scope by 50%\n3. Talked to 10 customers directly\n\nIt was uncomfortable, but it turned everything around."
        elif "HOOK" in system_prompt or "HOOK" in user_prompt:
            content = f"Most people fail at {topic_str} because they make this one basic mistake.\n\nHere is what nobody tells you until you've wasted 6 months doing it wrong.\n\nKeep it simple. Build daily. Track execution over ideas.\n\nConsistency wins every single time."
        elif "SHORTEN" in system_prompt or "SHORTEN" in user_prompt:
            content = f"Hard truth about {topic_str}:\n\n- Build less, test more.\n- Feedback beats perfection.\n- Execution is the only moat.\n\nStop overcomplicating it."
        elif "BUZZWORD" in system_prompt or "BUZZWORD" in user_prompt:
            content = f"Let's talk plainly about {topic_str}.\n\nNo buzzwords. No corporate jargon.\n\nIf you want to solve this problem, focus on three simple steps:\n1. Clear goals\n2. Daily practice\n3. Honest metrics\n\nThat is all it takes."
        else:
            content = (
                f"Most people overcomplicate {topic_str}.\n\n"
                f"I used to spend hours tweaking details that didn't matter. "
                f"Then I realized something critical: simplicity always outperforms complexity.\n\n"
                f"Here are 3 rules I follow now:\n\n"
                f"1. Cut out the fluff immediately\n"
                f"2. Focus on clear execution over big promises\n"
                f"3. Ask for honest feedback early\n\n"
                f"If you're working on {topic_str} today, start small and move fast."
            )

        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=used_model
        )
