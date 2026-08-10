import pytest
from pydantic import ValidationError
from app.schemas.post import GenerateRequest, RefineRequest
from app.prompts.prompt_builder import PromptBuilder


def test_generate_request_language_default():
    req = GenerateRequest(topic="3 months Python internship")
    assert req.language == "English"


def test_generate_request_language_valid_options():
    req_en = GenerateRequest(topic="Python internship", language="English")
    assert req_en.language == "English"

    req_hi = GenerateRequest(topic="Python internship", language="Hindi")
    assert req_hi.language == "Hindi"

    req_hing = GenerateRequest(topic="Python internship", language="Hinglish")
    assert req_hing.language == "Hinglish"


def test_generate_request_language_trim_and_fallback():
    req = GenerateRequest(topic="Python internship", language="  Hindi  ")
    assert req.language == "Hindi"

    req_empty = GenerateRequest(topic="Python internship", language="")
    assert req_empty.language == "English"


def test_generate_request_language_invalid():
    with pytest.raises(ValidationError):
        GenerateRequest(topic="Python internship", language="Spanish")


def test_prompt_builder_language_rendering():
    prompt_en = PromptBuilder.build_generation_prompt(
        topic="3 months Python internship",
        language="English"
    )
    assert "LANGUAGE:\nEnglish" in prompt_en
    assert "Write naturally in English." in prompt_en

    prompt_hi = PromptBuilder.build_generation_prompt(
        topic="3 months Python internship",
        language="Hindi"
    )
    assert "LANGUAGE:\nHindi" in prompt_hi
    assert "Devanagari script" in prompt_hi

    prompt_hing = PromptBuilder.build_generation_prompt(
        topic="3 months Python internship",
        language="Hinglish"
    )
    assert "LANGUAGE:\nHinglish" in prompt_hing
    assert "natural Indian Hinglish using Roman script" in prompt_hing
