"""MCP GitHub Client - wraps GitHub API calls with structured error handling"""
import httpx
import logging
from typing import Dict, Any, Optional
from ..config import settings

logger = logging.getLogger(__name__)


class MCPGitHubClient:
    """
    Client for GitHub API operations.
    
    This wraps the GitHub REST API and ensures all responses follow
    the standardized format with 'ok' field.
    """
    
    def __init__(self):
        self.base_url = settings.github_api_base_url
        self.owner = settings.github_owner
        self.repo = settings.github_repo
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-OS-MCP-Client/0.1.0"
        }
        
        if settings.github_pat:
            self.headers["Authorization"] = f"Bearer {settings.github_pat}"
    
    async def read_file(self, path: str, ref: str = "main") -> Dict[str, Any]:
        """
        Read a file from GitHub repository.
        
        Returns:
            {
                "ok": True/False,
                "content": "..." (if ok=True),
                "path": "...",
                "sha": "...",
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False),
                "status_code": ... (if ok=False)
            }
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        params = {"ref": ref}
        
        return await self._call_github(
            method="GET",
            url=url,
            params=params,
            operation_name="read_file"
        )
    
    async def list_tree(
        self, 
        path: str = "", 
        ref: str = "main", 
        recursive: bool = False
    ) -> Dict[str, Any]:
        """
        List repository tree at a given path.
        
        Returns:
            {
                "ok": True/False,
                "tree": [...] (if ok=True),
                "path": "...",
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False),
                "status_code": ... (if ok=False)
            }
        """
        # For tree listing, we use the Git Trees API
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/git/trees/{ref}"
        
        if path:
            url += f":{path}"
        
        params = {}
        if recursive:
            params["recursive"] = "1"
        
        return await self._call_github(
            method="GET",
            url=url,
            params=params,
            operation_name="list_tree"
        )
    
    async def create_branch(self, branch_name: str, base_ref: str = "main") -> Dict[str, Any]:
        """
        Create a new branch from a base ref.
        
        Returns:
            {
                "ok": True/False,
                "branch_name": "...",
                "sha": "..." (if ok=True),
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False)
            }
        """
        # First, get the SHA of the base ref
        ref_url = f"{self.base_url}/repos/{self.owner}/{self.repo}/git/ref/heads/{base_ref}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                ref_response = await client.get(ref_url, headers=self.headers)
                
                if ref_response.status_code != 200:
                    return {
                        "ok": False,
                        "error_type": "base_ref_not_found",
                        "message": f"Base ref '{base_ref}' not found",
                        "status_code": ref_response.status_code
                    }
                
                base_sha = ref_response.json()["object"]["sha"]
                
                # Now create the new branch
                create_url = f"{self.base_url}/repos/{self.owner}/{self.repo}/git/refs"
                payload = {
                    "ref": f"refs/heads/{branch_name}",
                    "sha": base_sha
                }
                
                create_response = await client.post(
                    create_url, 
                    headers=self.headers, 
                    json=payload
                )
                
                if create_response.status_code in [200, 201]:
                    return {
                        "ok": True,
                        "branch_name": branch_name,
                        "sha": base_sha,
                        "message": f"Branch '{branch_name}' created successfully"
                    }
                else:
                    error_data = create_response.json()
                    return {
                        "ok": False,
                        "error_type": "branch_creation_failed",
                        "message": error_data.get("message", "Failed to create branch"),
                        "status_code": create_response.status_code
                    }
            
            except httpx.TimeoutException:
                return {
                    "ok": False,
                    "error_type": "timeout",
                    "message": "Request to GitHub API timed out"
                }
            except Exception as e:
                logger.error(f"Error creating branch: {str(e)}")
                return {
                    "ok": False,
                    "error_type": "unknown_error",
                    "message": str(e)
                }
    
    async def update_file(
        self, 
        path: str, 
        content: str, 
        branch: str,
        message: str,
        sha: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update a file on a branch.
        
        Returns:
            {
                "ok": True/False,
                "path": "...",
                "sha": "..." (if ok=True),
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False)
            }
        """
        import base64
        
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        
        # Encode content to base64
        encoded_content = base64.b64encode(content.encode()).decode()
        
        payload = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }
        
        if sha:
            payload["sha"] = sha
        
        return await self._call_github(
            method="PUT",
            url=url,
            json_data=payload,
            operation_name="update_file"
        )
    
    async def create_pull_request(
        self,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> Dict[str, Any]:
        """
        Create a pull request.
        
        Returns:
            {
                "ok": True/False,
                "pr_number": ... (if ok=True),
                "pr_url": "..." (if ok=True),
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False)
            }
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls"
        
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        
        result = await self._call_github(
            method="POST",
            url=url,
            json_data=payload,
            operation_name="create_pull_request"
        )
        
        # Extract PR number and URL if successful
        if result.get("ok") and "number" in result:
            result["pr_number"] = result.pop("number")
            result["pr_url"] = result.pop("html_url", "")
        
        return result
    
    async def _call_github(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        operation_name: str = "github_api_call"
    ) -> Dict[str, Any]:
        """
        Internal method to call GitHub API with standardized error handling.
        
        All responses are normalized to include 'ok' field.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                logger.info(f"GitHub API call: {method} {url}")
                
                request_kwargs = {"headers": self.headers}
                if params:
                    request_kwargs["params"] = params
                if json_data:
                    request_kwargs["json"] = json_data
                
                response = await client.request(method, url, **request_kwargs)
                
                # Handle error status codes
                if response.status_code >= 400:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except Exception:
                        pass
                    
                    return {
                        "ok": False,
                        "error_type": f"http_{response.status_code}",
                        "message": error_data.get("message", f"GitHub API returned {response.status_code}"),
                        "status_code": response.status_code
                    }
                
                # Success case
                response_data = response.json()
                
                # Ensure 'ok' field exists
                if "ok" not in response_data:
                    response_data["ok"] = True
                
                return response_data
            
            except httpx.TimeoutException:
                logger.error(f"{operation_name}: Request timed out")
                return {
                    "ok": False,
                    "error_type": "timeout",
                    "message": "Request to GitHub API timed out",
                    "status_code": 408
                }
            
            except Exception as e:
                logger.error(f"{operation_name}: Unexpected error: {str(e)}")
                return {
                    "ok": False,
                    "error_type": "unknown_error",
                    "message": str(e),
                    "status_code": 500
                }
