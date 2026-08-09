import pytest
from app.prompts import PromptBuilder
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


def test_system_prompt_banned_phrases_and_rules():
    system_prompt = PromptBuilder.get_system_prompt()
    
    # Assert anti-hallucination rules exist
    assert "USE ONLY THE USER'S ACTUAL INFORMATION" in system_prompt
    assert "NEVER INVENT personal experiences" in system_prompt
    assert "NEVER INVENT achievements" in system_prompt
    assert "NEVER INVENT statistics" in system_prompt
    assert "NEVER INVENT names, client details, or company names" in system_prompt

    # Assert banned phrases are explicitly listed
    banned_phrases = [
        "I'm thrilled to announce...",
        "I'm excited to share...",
        "I'm delighted to...",
        "Today, I want to share...",
        "In today's fast-paced world...",
        "Game changer",
        "Unlock your potential",
        "Leverage",
        "Embark on a journey",
        "At the end of the day",
        "Revolutionize"
    ]
    for phrase in banned_phrases:
        assert phrase in system_prompt, f"Missing banned phrase: {phrase}"


def test_build_generation_prompt_parameter_injection():
    prompt = PromptBuilder.build_generation_prompt(
        topic="Building an AI SaaS in 14 days",
        post_type="Project",
        tone="Conversational",
        target_audience="Software Engineers & Founders",
        personal_context="Worked 12 hours a day without external funding",
        key_points="Focus on user feedback, ship fast",
        length="Short"
    )

    assert "Building an AI SaaS in 14 days" in prompt
    assert "Project" in prompt
    assert "Conversational" in prompt
    assert "Software Engineers & Founders" in prompt
    assert "Worked 12 hours a day without external funding" in prompt
    assert "Focus on user feedback, ship fast" in prompt
    assert "Short & concise" in prompt


@pytest.mark.asyncio
async def test_multiple_generation_examples():
    examples = [
        GenerateRequest(
            topic="Lessons from 50 customer interviews",
            post_type="Educational",
            tone="Thoughtful",
            target_audience="Product Managers",
            personal_context="Interviewed 50 B2B SaaS buyers",
            key_points="Listen 80% of the time, don't pitch solution early",
            length="Medium",
            provider="mock"
        ),
        GenerateRequest(
            topic="My biggest career failure and recovery",
            post_type="Career",
            tone="Storytelling",
            target_audience="Junior Developers",
            personal_context="Got rejected from 10 companies before landing first role",
            key_points="Build side projects, don't give up",
            length="Long",
            provider="mock"
        ),
        GenerateRequest(
            topic="Why simple code beats clever code",
            post_type="Opinion",
            tone="Confident",
            target_audience="Engineers",
            key_points="Readability over micro-optimizations",
            length="Short",
            provider="mock"
        )
    ]

    for req in examples:
        response = await PostService.generate_post(req)
        assert response.post is not None
        assert len(response.post) > 20
        assert response.metadata["word_count"] > 0
        assert response.metadata["topic"] == req.topic
