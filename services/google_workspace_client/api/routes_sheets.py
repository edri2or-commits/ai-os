"""Sheets API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any
from ..models.schemas import (
    CreateSheetRequest,
    CreateSheetResponse,
    ReadSheetRequest,
    ReadSheetResponse
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/sheets", tags=["sheets"])


@router.post("/create", response_model=CreateSheetResponse)
async def create_sheet(request: CreateSheetRequest) -> Dict[str, Any]:
    """
    Create a new spreadsheet.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Creating spreadsheet: {request.title}")
    
    if not google_client.is_authenticated():
        return CreateSheetResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Create spreadsheet
        spreadsheet = {
            'properties': {
                'title': request.title
            }
        }
        
        result = google_client.sheets.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId,spreadsheetUrl'
        ).execute()
        
        return CreateSheetResponse(
            ok=True,
            spreadsheet_id=result.get('spreadsheetId'),
            spreadsheet_url=result.get('spreadsheetUrl'),
            message="Spreadsheet created successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to create spreadsheet: {e}")
        return CreateSheetResponse(
            ok=False,
            error_type="create_failed",
            message=str(e)
        )


@router.post("/read", response_model=ReadSheetResponse)
async def read_sheet(request: ReadSheetRequest) -> Dict[str, Any]:
    """
    Read data from a spreadsheet.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Reading spreadsheet: {request.spreadsheet_id}, range: {request.range}")
    
    if not google_client.is_authenticated():
        return ReadSheetResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Read spreadsheet
        result = google_client.sheets.spreadsheets().values().get(
            spreadsheetId=request.spreadsheet_id,
            range=request.range
        ).execute()
        
        values = result.get('values', [])
        
        return ReadSheetResponse(
            ok=True,
            values=values,
            message=f"Read {len(values)} rows"
        )
    
    except Exception as e:
        logger.error(f"Failed to read spreadsheet: {e}")
        return ReadSheetResponse(
            ok=False,
            error_type="read_failed",
            message=str(e)
        )
