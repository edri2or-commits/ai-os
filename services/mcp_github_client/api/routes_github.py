"""GitHub operations API routes"""
import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..models import (
    ReadFileRequest,
    ReadFileResponse,
    ListTreeRequest,
    ListTreeResponse,
    OpenPRRequest,
    OpenPRResponse,
)
from ..core import MCPGitHubClient, OpenAIClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/github", tags=["github"])

# Initialize clients
github_client = MCPGitHubClient()
openai_client = OpenAIClient()


@router.post("/read-file", response_model=ReadFileResponse)
async def read_file(request: ReadFileRequest) -> Dict[str, Any]:
    """
    Read a file from the GitHub repository.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Reading file: {request.path} (ref: {request.ref})")
    
    result = await github_client.read_file(
        path=request.path,
        ref=request.ref
    )
    
    # If successful, extract content from GitHub's response
    if result.get("ok"):
        import base64
        
        # GitHub returns base64-encoded content
        if "content" in result:
            try:
                decoded_content = base64.b64decode(result["content"]).decode("utf-8")
                return ReadFileResponse(
                    ok=True,
                    content=decoded_content,
                    path=request.path,
                    sha=result.get("sha"),
                    message="File read successfully"
                )
            except Exception as e:
                logger.error(f"Failed to decode file content: {str(e)}")
                return ReadFileResponse(
                    ok=False,
                    error_type="decode_error",
                    message=f"Failed to decode file content: {str(e)}"
                )
    
    # Error case - pass through the error from github_client
    return ReadFileResponse(
        ok=False,
        error_type=result.get("error_type", "unknown_error"),
        message=result.get("message", "Failed to read file"),
        status_code=result.get("status_code")
    )


@router.post("/list-tree", response_model=ListTreeResponse)
async def list_tree(request: ListTreeRequest) -> Dict[str, Any]:
    """
    List files in the repository tree.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Listing tree: {request.path} (ref: {request.ref}, recursive: {request.recursive})")
    
    result = await github_client.list_tree(
        path=request.path,
        ref=request.ref,
        recursive=request.recursive
    )
    
    if result.get("ok"):
        return ListTreeResponse(
            ok=True,
            tree=result.get("tree", []),
            path=request.path,
            message="Tree listed successfully"
        )
    
    # Error case
    return ListTreeResponse(
        ok=False,
        error_type=result.get("error_type", "unknown_error"),
        message=result.get("message", "Failed to list tree"),
        status_code=result.get("status_code")
    )


@router.post("/open-pr", response_model=OpenPRResponse)
async def open_pr(request: OpenPRRequest) -> Dict[str, Any]:
    """
    Open a Pull Request with file changes.
    
    This is the ONLY way to make changes to the repository - all changes
    must go through a PR workflow.
    
    Process:
    1. Create a new branch from base_branch
    2. Apply file changes to the new branch
    3. Create a PR from new branch to base_branch
    4. (Optional) Use AI to refine PR description
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Opening PR: {request.title} (base: {request.base_branch})")
    
    # Step 1: Create a unique branch name
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"ai-os-pr-{timestamp}"
    
    logger.info(f"Creating branch: {branch_name}")
    branch_result = await github_client.create_branch(
        branch_name=branch_name,
        base_ref=request.base_branch
    )
    
    if not branch_result.get("ok"):
        return OpenPRResponse(
            ok=False,
            error_type=branch_result.get("error_type", "branch_creation_failed"),
            message=f"Failed to create branch: {branch_result.get('message')}"
        )
    
    # Step 2: Apply file changes to the new branch
    for file_change in request.files:
        logger.info(f"Updating file: {file_change.path} (operation: {file_change.operation})")
        
        # For update operations, we need the current file SHA
        sha = None
        if file_change.operation == "update":
            read_result = await github_client.read_file(
                path=file_change.path,
                ref=request.base_branch
            )
            if read_result.get("ok"):
                sha = read_result.get("sha")
        
        update_result = await github_client.update_file(
            path=file_change.path,
            content=file_change.content,
            branch=branch_name,
            message=f"[AI-OS] {file_change.operation} {file_change.path}",
            sha=sha
        )
        
        if not update_result.get("ok"):
            return OpenPRResponse(
                ok=False,
                error_type=update_result.get("error_type", "file_update_failed"),
                message=f"Failed to update {file_change.path}: {update_result.get('message')}"
            )
    
    # Step 3: Optionally refine PR description with AI
    pr_description = request.description
    
    if request.use_ai_generation:
        logger.info("Using AI to generate PR description")
        files_summary = "\n".join([f"- {f.path} ({f.operation})" for f in request.files])
        
        ai_result = await openai_client.generate_pr_description(
            title=request.title,
            files_summary=files_summary,
            base_description=request.description
        )
        
        if ai_result.get("ok"):
            pr_description = ai_result.get("content", pr_description)
        else:
            logger.warning(f"AI generation failed, using original description: {ai_result.get('message')}")
    
    # Step 4: Create the Pull Request
    logger.info(f"Creating PR from {branch_name} to {request.base_branch}")
    pr_result = await github_client.create_pull_request(
        title=request.title,
        body=pr_description,
        head=branch_name,
        base=request.base_branch
    )
    
    if pr_result.get("ok"):
        return OpenPRResponse(
            ok=True,
            pr_number=pr_result.get("pr_number"),
            pr_url=pr_result.get("pr_url"),
            branch_name=branch_name,
            message="Pull Request created successfully"
        )
    
    # Error case
    return OpenPRResponse(
        ok=False,
        error_type=pr_result.get("error_type", "pr_creation_failed"),
        message=f"Failed to create PR: {pr_result.get('message')}"
    )
