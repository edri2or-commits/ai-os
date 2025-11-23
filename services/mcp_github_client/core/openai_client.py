"""OpenAI Client for AI-powered PR content generation"""
import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from ..config import settings

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Client for OpenAI API to generate/refine PR content.
    
    This is OPTIONAL - only used if use_ai_generation=True in OpenPRRequest.
    """
    
    def __init__(self):
        self.client = None
        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
    
    async def generate_pr_description(
        self,
        title: str,
        files_summary: str,
        base_description: str = ""
    ) -> Dict[str, Any]:
        """
        Use AI to generate/refine PR description.
        
        Returns:
            {
                "ok": True/False,
                "content": "..." (if ok=True),
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False)
            }
        """
        if not self.client:
            return {
                "ok": False,
                "error_type": "openai_not_configured",
                "message": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""You are helping to write a Pull Request description.

PR Title: {title}

Files Changed:
{files_summary}

Base Description:
{base_description or "No description provided"}

Generate a clear, professional PR description that:
1. Summarizes what changed and why
2. Highlights key technical decisions
3. Notes any breaking changes or dependencies
4. Is concise but informative

Return only the PR description text, no extra commentary."""

            logger.info("Calling OpenAI API to generate PR description")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical writer helping with PR descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            return {
                "ok": True,
                "content": content,
                "message": "PR description generated successfully"
            }
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                "ok": False,
                "error_type": "openai_api_error",
                "message": str(e)
            }
    
    async def generate_file_update(
        self,
        file_path: str,
        current_content: str,
        update_instructions: str
    ) -> Dict[str, Any]:
        """
        Use AI to generate updated file content based on instructions.
        
        Returns:
            {
                "ok": True/False,
                "content": "..." (if ok=True),
                "error_type": "..." (if ok=False),
                "message": "..." (if ok=False)
            }
        """
        if not self.client:
            return {
                "ok": False,
                "error_type": "openai_not_configured",
                "message": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""You are helping to update a file in a codebase.

File: {file_path}

Current Content:
```
{current_content}
```

Update Instructions:
{update_instructions}

Generate the COMPLETE updated file content. Return ONLY the file content, no explanations."""

            logger.info(f"Calling OpenAI API to update file: {file_path}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a code assistant helping with file updates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code fences if present
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines)
            
            return {
                "ok": True,
                "content": content,
                "message": "File content generated successfully"
            }
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                "ok": False,
                "error_type": "openai_api_error",
                "message": str(e)
            }
