"""Pydantic models for request/response schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ============================================================================
# Standard Response Models (always include 'ok' field)
# ============================================================================

class BaseResponse(BaseModel):
    """Base response model - all responses inherit from this"""
    ok: bool = Field(..., description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Human-readable message")
    error_type: Optional[str] = Field(None, description="Error type if ok=False")
    status_code: Optional[int] = Field(None, description="HTTP status code if relevant")


class ReadFileResponse(BaseResponse):
    """Response for reading a file from GitHub"""
    content: Optional[str] = Field(None, description="File content (if ok=True)")
    path: Optional[str] = Field(None, description="File path that was read")
    sha: Optional[str] = Field(None, description="Git SHA of the file")


class ListTreeResponse(BaseResponse):
    """Response for listing repository tree"""
    tree: Optional[List[Dict[str, Any]]] = Field(None, description="List of tree items")
    path: Optional[str] = Field(None, description="Path that was listed")


class OpenPRResponse(BaseResponse):
    """Response for opening a Pull Request"""
    pr_number: Optional[int] = Field(None, description="PR number (if ok=True)")
    pr_url: Optional[str] = Field(None, description="PR URL (if ok=True)")
    branch_name: Optional[str] = Field(None, description="Branch name created")


# ============================================================================
# Request Models
# ============================================================================

class ReadFileRequest(BaseModel):
    """Request to read a file from GitHub"""
    path: str = Field(..., description="Path to the file in the repository")
    ref: str = Field(default="main", description="Git ref (branch/tag/commit)")


class ListTreeRequest(BaseModel):
    """Request to list repository tree"""
    path: str = Field(default="", description="Path to list (empty = root)")
    ref: str = Field(default="main", description="Git ref (branch/tag/commit)")
    recursive: bool = Field(default=False, description="Whether to list recursively")


class FileChange(BaseModel):
    """A single file change for a PR"""
    path: str = Field(..., description="File path")
    content: str = Field(..., description="New file content")
    operation: str = Field(default="update", description="Operation: create/update/delete")


class OpenPRRequest(BaseModel):
    """Request to open a Pull Request"""
    title: str = Field(..., description="PR title")
    description: str = Field(..., description="PR description")
    files: List[FileChange] = Field(..., description="List of file changes")
    base_branch: str = Field(default="main", description="Base branch to merge into")
    use_ai_generation: bool = Field(
        default=False, 
        description="Whether to use AI to refine PR content"
    )


class WriteFileRequest(BaseModel):
    """Request to write a file directly to main branch"""
    path: str = Field(..., description="File path in the repository")
    content: str = Field(..., description="File content")
    message: str = Field(..., description="Commit message")
    branch: str = Field(default="main", description="Branch to write to")


class WriteFileResponse(BaseResponse):
    """Response for writing a file"""
    path: Optional[str] = Field(None, description="File path that was written")
    sha: Optional[str] = Field(None, description="New commit SHA")
    commit_url: Optional[str] = Field(None, description="URL to the commit")


class DeleteFileRequest(BaseModel):
    """Request to delete a file"""
    path: str = Field(..., description="File path to delete")
    message: str = Field(..., description="Commit message")
    branch: str = Field(default="main", description="Branch to delete from")


class DeleteFileResponse(BaseResponse):
    """Response for deleting a file"""
    path: Optional[str] = Field(None, description="File path that was deleted")


class ListBranchesResponse(BaseResponse):
    """Response for listing branches"""
    branches: Optional[List[Dict[str, Any]]] = Field(None, description="List of branches")


class GetCommitsRequest(BaseModel):
    """Request to get commits"""
    path: Optional[str] = Field(None, description="Filter by file path")
    branch: str = Field(default="main", description="Branch to get commits from")
    limit: int = Field(default=10, description="Number of commits to return")


class GetCommitsResponse(BaseResponse):
    """Response for getting commits"""
    commits: Optional[List[Dict[str, Any]]] = Field(None, description="List of commits")
