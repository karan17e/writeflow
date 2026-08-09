import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "llm_provider" in data


@pytest.mark.asyncio
async def test_generate_and_refine_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        gen_payload = {
            "topic": "Building in public as a solo developer",
            "post_type": "Story",
            "tone": "Casual",
            "personal_context": "Built a app in 7 days",
            "key_points": "Focus on MVP, listen to users",
            "length": "Medium",
            "provider": "mock"
        }
        res_gen = await ac.post("/api/generate", json=gen_payload)
        assert res_gen.status_code == 200
        data = res_gen.json()
        assert "post" in data
        assert "metadata" in data
