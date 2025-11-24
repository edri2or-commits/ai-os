"""Tasks API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any
from ..models.schemas import (
    CreateTaskRequest,
    CreateTaskResponse
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/tasks", tags=["tasks"])


@router.post("/create", response_model=CreateTaskResponse)
async def create_task(request: CreateTaskRequest) -> Dict[str, Any]:
    """
    Create a new task.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Creating task: {request.title}")
    
    if not google_client.is_authenticated():
        return CreateTaskResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Get default task list
        tasklists = google_client.tasks.tasklists().list().execute()
        if not tasklists.get('items'):
            return CreateTaskResponse(
                ok=False,
                error_type="no_tasklist",
                message="No task lists found"
            )
        
        tasklist_id = tasklists['items'][0]['id']
        
        # Create task
        task = {
            'title': request.title
        }
        
        if request.notes:
            task['notes'] = request.notes
        
        if request.due:
            task['due'] = request.due
        
        result = google_client.tasks.tasks().insert(
            tasklist=tasklist_id,
            body=task
        ).execute()
        
        return CreateTaskResponse(
            ok=True,
            task_id=result.get('id'),
            message="Task created successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return CreateTaskResponse(
            ok=False,
            error_type="create_failed",
            message=str(e)
        )
