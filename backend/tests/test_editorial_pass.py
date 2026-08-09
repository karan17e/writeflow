import pytest
from app.prompts import PromptBuilder
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


def test_editor_pass_prompt_checklist_and_constraints():
    prompt = PromptBuilder.build_editor_pass_prompt("Sample AI draft post content")
    prompt_lower = prompt.lower()
    
    # Assert all 10 checklist review areas are present
    assert "generic ai language" in prompt_lower
    assert "corporate buzzwords" in prompt_lower
    assert "repetitive sentence structures" in prompt_lower
    assert "artificial transitions" in prompt_lower
    assert "excessive enthusiasm" in prompt_lower
    assert "unnecessary emojis" in prompt_lower
    assert "excessive hashtags" in prompt_lower
    assert "empty motivational statements" in prompt_lower
    assert "lack of specificity" in prompt_lower
    assert "overly formal language" in prompt_lower

    # Assert preservation rules
    assert "PRESERVE the original meaning" in prompt
    assert "PRESERVE all factual information" in prompt
    assert "NEVER INVENT new statistics" in prompt
    assert "Sample AI draft post content" in prompt


@pytest.mark.asyncio
async def test_two_stage_generation_pipeline():
    req = GenerateRequest(
        topic="Scaling engineering teams with remote developers",
        post_type="Educational",
        tone="Conversational",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    
    assert response.post is not None
    assert len(response.post) > 20
    assert response.metadata["editorial_pass"] is True
    assert response.metadata["action"] == "generate"
