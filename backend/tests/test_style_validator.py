import pytest
from app.services.style_validator import (
    parse_user_style_instructions,
    validate_style_requirements,
    count_emojis,
    count_hashtags
)
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService


def test_parse_user_style_instructions():
    parsed_1 = parse_user_style_instructions("Use 6 emojis and short sentences")
    assert parsed_1.get("emoji_count") == 6

    parsed_2 = parse_user_style_instructions("Use no emojis, 3 hashtags, keep under 150 words")
    assert parsed_2.get("emoji_count") == 0
    assert parsed_2.get("hashtag_count") == 3
    assert parsed_2.get("max_words") == 150


def test_validate_style_requirements():
    text_with_emojis = "I completed my Python internship! 🐍 💻 🚀 🧠 📚 🎯"
    requirements = {"emoji_count": 6}
    report = validate_style_requirements(text_with_emojis, requirements)
    assert report["valid"] is True
    assert report["details"]["emoji_count"]["actual"] == 6


@pytest.mark.asyncio
async def test_style_requirement_test_1_six_emojis():
    req = GenerateRequest(
        topic="3 months Python internship",
        writing_style="Use 6 emojis",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "3 months Python internship"
    assert response.metadata["parsed_style_requirements"].get("emoji_count") == 6


@pytest.mark.asyncio
async def test_style_requirement_test_2_no_emojis():
    req = GenerateRequest(
        topic="3 months Python internship",
        writing_style="Use no emojis",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["parsed_style_requirements"].get("emoji_count") == 0


@pytest.mark.asyncio
async def test_style_requirement_test_3_three_emojis():
    req = GenerateRequest(
        topic="My first hackathon",
        writing_style="Use 3 emojis and short sentences",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["parsed_style_requirements"].get("emoji_count") == 3


@pytest.mark.asyncio
async def test_style_requirement_test_4_no_hashtags():
    req = GenerateRequest(
        topic="Learning C++",
        writing_style="Use simple language and no hashtags",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["parsed_style_requirements"].get("hashtag_count") == 0


@pytest.mark.asyncio
async def test_style_requirement_test_5_two_emojis_max_words():
    req = GenerateRequest(
        topic="Building an AI resume analyzer",
        writing_style="Use 2 emojis and keep it under 150 words",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["parsed_style_requirements"].get("emoji_count") == 2
    assert response.metadata["parsed_style_requirements"].get("max_words") == 150
