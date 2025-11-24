"""Drive API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any
from ..models.schemas import (
    SearchDriveRequest,
    SearchDriveResponse,
    DriveFile
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/drive", tags=["drive"])


@router.post("/search", response_model=SearchDriveResponse)
async def search_drive(request: SearchDriveRequest) -> Dict[str, Any]:
    """
    Search Google Drive.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Searching Drive: {request.query}")
    
    if not google_client.is_authenticated():
        return SearchDriveResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Search Drive
        results = google_client.drive.files().list(
            q=f"name contains '{request.query}'",
            pageSize=request.max_results,
            fields="files(id, name, mimeType, webViewLink, createdTime)"
        ).execute()
        
        files = results.get('files', [])
        
        # Convert to DriveFile objects
        drive_files = []
        for file in files:
            drive_files.append(DriveFile(
                id=file['id'],
                name=file['name'],
                mime_type=file.get('mimeType'),
                web_view_link=file.get('webViewLink'),
                created_time=file.get('createdTime')
            ))
        
        return SearchDriveResponse(
            ok=True,
            files=drive_files,
            message=f"Found {len(drive_files)} files"
        )
    
    except Exception as e:
        logger.error(f"Failed to search Drive: {e}")
        return SearchDriveResponse(
            ok=False,
            error_type="search_failed",
            message=str(e)
        )
