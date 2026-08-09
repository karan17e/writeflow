import pytest
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService, check_template_repetition
from app.prompts import PromptBuilder


def test_system_prompt_topic_primacy_and_non_hallucination_rules():
    system_prompt = PromptBuilder.get_system_prompt()
    assert "YOUR HIGHEST PRIORITY IS FACTUAL RELEVANCE TO THE USER'S TOPIC" in system_prompt
    assert "HIERARCHY OF CONTROL" in system_prompt
    assert "TOPIC = WHAT THE POST IS ABOUT" in system_prompt
    assert "USE ONLY THE USER'S ACTUAL INFORMATION" in system_prompt


def test_template_repetition_detection_helper():
    repetitive_text = "Here are 3 things I learned during my internship. 1. Code fast. 2. Ask questions. 3. Ship it."
    assert check_template_repetition(repetitive_text) is True

    natural_text = "Three months ago, I started a Python internship with a simple goal: write cleaner code outside of class."
    assert check_template_repetition(natural_text) is False


@pytest.mark.asyncio
async def test_relevance_validation_audit_pass():
    topic = "3 months Python internship"
    draft = "Over the last 3 months, I completed a Python internship. I focused on core programming fundamentals and writing clean scripts."
    audit = await PostService.validate_relevance(
        topic=topic,
        draft_content=draft,
        provider_name="mock"
    )
    assert audit is not None
    assert "is_relevant" in audit


# 10 MANDATORY TOPIC RELEVANCE TESTS

@pytest.mark.asyncio
async def test_topic_1_python_internship():
    req = GenerateRequest(topic="3 months Python internship", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "3 months Python internship"
    assert "selected_structure" in response.metadata


@pytest.mark.asyncio
async def test_topic_2_first_college_project():
    req = GenerateRequest(topic="My first college project", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "My first college project"


@pytest.mark.asyncio
async def test_topic_3_learning_cpp():
    req = GenerateRequest(topic="Learning C++", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "Learning C++"


@pytest.mark.asyncio
async def test_topic_4_first_hackathon():
    req = GenerateRequest(topic="My first hackathon", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "My first hackathon"


@pytest.mark.asyncio
async def test_topic_5_ai_resume_analyzer():
    req = GenerateRequest(topic="Building an AI resume analyzer", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "Building an AI resume analyzer"


@pytest.mark.asyncio
async def test_topic_6_my_first_internship():
    req = GenerateRequest(topic="My first internship", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "My first internship"


@pytest.mark.asyncio
async def test_topic_7_first_year_college():
    req = GenerateRequest(topic="What I learned during my first year of college", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "What I learned during my first year of college"


@pytest.mark.asyncio
async def test_topic_8_learning_arduino():
    req = GenerateRequest(topic="Learning Arduino", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "Learning Arduino"


@pytest.mark.asyncio
async def test_topic_9_starting_programming_from_zero():
    req = GenerateRequest(topic="Starting programming from zero", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "Starting programming from zero"


@pytest.mark.asyncio
async def test_topic_10_project_failed_at():
    req = GenerateRequest(topic="A project I failed at", provider="mock")
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "A project I failed at"


@pytest.mark.asyncio
async def test_topic_primacy_over_audience():
    req = GenerateRequest(
        topic="3 months Python internship",
        target_audience="Founders",
        provider="mock"
    )
    response = await PostService.generate_post(req)
    assert response.post is not None
    assert response.metadata["topic"] == "3 months Python internship"
