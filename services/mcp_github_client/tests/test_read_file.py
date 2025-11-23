"""Tests for read_file endpoint"""
import pytest
from httpx import AsyncClient
from ..main import app


@pytest.mark.asyncio
async def test_read_file_success():
    """Test successful file read - expects 'ok' field"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/github/read-file",
            json={"path": "README.md", "ref": "main"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Critical: response must have 'ok' field
        assert "ok" in data
        
        if data["ok"]:
            # Success case - must have content
            assert "content" in data
            assert isinstance(data["content"], str)
            assert data["path"] == "README.md"
        else:
            # Error case - must have error_type and message
            assert "error_type" in data
            assert "message" in data


@pytest.mark.asyncio
async def test_read_file_not_found():
    """Test reading non-existent file - expects standardized error"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/github/read-file",
            json={"path": "nonexistent_file_12345.txt", "ref": "main"}
        )
        
        assert response.status_code == 200  # We return 200 with ok=False
        data = response.json()
        
        # Critical: response must have 'ok' field
        assert "ok" in data
        assert data["ok"] is False
        
        # Must have error information
        assert "error_type" in data
        assert "message" in data
        assert "status_code" in data


@pytest.mark.asyncio
async def test_list_tree_success():
    """Test successful tree listing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/github/list-tree",
            json={"path": "", "ref": "main", "recursive": False}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Critical: response must have 'ok' field
        assert "ok" in data


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["ok"] is True
        assert "service" in data
