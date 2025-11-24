"""GitHub operations API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/read-file")
async def read_file_placeholder():
    """GitHub integration placeholder - will be implemented"""
    return {
        "ok": False,
        "error_type": "not_implemented",
        "message": "GitHub integration coming soon - use MCP GitHub Client on port 8081"
    }


@router.post("/list-tree")
async def list_tree_placeholder():
    """GitHub integration placeholder - will be implemented"""
    return {
        "ok": False,
        "error_type": "not_implemented",
        "message": "GitHub integration coming soon - use MCP GitHub Client on port 8081"
    }


@router.post("/open-pr")
async def open_pr_placeholder():
    """GitHub integration placeholder - will be implemented"""
    return {
        "ok": False,
        "error_type": "not_implemented",
        "message": "GitHub integration coming soon - use MCP GitHub Client on port 8081"
    }
