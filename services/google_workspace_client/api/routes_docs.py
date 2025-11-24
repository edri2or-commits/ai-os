"""Docs API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any
from ..models.schemas import (
    CreateDocRequest,
    CreateDocResponse
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/docs", tags=["docs"])


@router.post("/create", response_model=CreateDocResponse)
async def create_doc(request: CreateDocRequest) -> Dict[str, Any]:
    """
    Create a new Google Doc.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Creating doc: {request.title}")
    
    if not google_client.is_authenticated():
        return CreateDocResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Create document
        doc = {
            'title': request.title
        }
        
        result = google_client.docs.documents().create(body=doc).execute()
        
        doc_id = result.get('documentId')
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        
        return CreateDocResponse(
            ok=True,
            document_id=doc_id,
            document_url=doc_url,
            message="Document created successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to create document: {e}")
        return CreateDocResponse(
            ok=False,
            error_type="create_failed",
            message=str(e)
        )
