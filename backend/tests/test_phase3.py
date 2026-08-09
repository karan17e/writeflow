import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.schemas.post import GenerateRequest, RefineRequest, PostResponse
from app.services.post_service import PostService
from app.configuration import settings


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_generate_post_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "topic": "Building SaaS in 30 days",
            "post_type": "Project",
            "tone": "Conversational",
            "provider": "mock"
        }
        response = await ac.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "post" in data
    assert "metadata" in data
    assert data["metadata"]["topic"] == payload["topic"]


@pytest.mark.asyncio
async def test_rewrite_post_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "post": "Here is an original draft post about my journey.",
            "additional_instructions": "Make it punchier",
            "provider": "mock"
        }
        response = await ac.post("/api/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "post" in data


@pytest.mark.asyncio
async def test_improve_hook_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "post": "Here is an original draft post about my journey.",
            "provider": "mock"
        }
        response = await ac.post("/api/improve-hook", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "post" in data


@pytest.mark.asyncio
async def test_humanize_post_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "post": "Here is an original draft post about my journey.",
            "provider": "mock"
        }
        response = await ac.post("/api/humanize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "post" in data


@pytest.mark.asyncio
async def test_shorten_post_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "post": "Here is an original draft post about my journey that is quite long.",
            "provider": "mock"
        }
        response = await ac.post("/api/shorten", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "post" in data


@pytest.mark.asyncio
async def test_missing_groq_api_key_configuration_error(monkeypatch):
    monkeypatch.setattr(settings, "GROQ_API_KEY", "")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "topic": "Building products",
            "provider": "groq"
        }
        response = await ac.post("/api/generate", json=payload)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert "GROQ_API_KEY is not configured" in detail


@pytest.mark.asyncio
async def test_validation_error_handling():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "topic": "a"
        }
        response = await ac.post("/api/generate", json=payload)
    assert response.status_code == 422
