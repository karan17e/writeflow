import pytest
from app.prompts import PromptBuilder
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


def test_system_prompt_public_figure_imitation_guardrail():
    system_prompt = PromptBuilder.get_system_prompt()
    assert "DO NOT IMITATE ANY SPECIFIC PUBLIC FIGURE, CELEBRITY, INFLUENCER, OR LIVING PERSON'S WRITING STYLE" in system_prompt


def test_generation_prompt_writing_style_injection():
    style = "My writing is simple and direct. I use short sentences. I don't use many emojis."
    prompt = PromptBuilder.build_generation_prompt(
        topic="Building software",
        writing_style=style
    )
    assert "USER'S PERSONAL WRITING STYLE CHARACTERISTICS" in prompt
    assert style in prompt


@pytest.mark.asyncio
async def test_generate_post_with_writing_style():
    req = GenerateRequest(
        topic="Building an API",
        writing_style="I write with very short punchy lines and no corporate jargon.",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["has_custom_writing_style"] is True
