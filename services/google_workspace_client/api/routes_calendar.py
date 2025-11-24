"""Calendar API routes"""
import logging
from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from ..models.schemas import (
    CreateEventRequest,
    CreateEventResponse,
    ListEventsRequest,
    ListEventsResponse,
    EventSummary
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/calendar", tags=["calendar"])


@router.post("/create-event", response_model=CreateEventResponse)
async def create_event(request: CreateEventRequest) -> Dict[str, Any]:
    """
    Create a calendar event.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Creating event: {request.summary}")
    
    if not google_client.is_authenticated():
        return CreateEventResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Build event
        event = {
            'summary': request.summary,
            'start': {
                'dateTime': request.start_time,
            },
            'end': {
                'dateTime': request.end_time,
            },
        }
        
        if request.description:
            event['description'] = request.description
        
        if request.location:
            event['location'] = request.location
        
        if request.attendees:
            event['attendees'] = [{'email': email} for email in request.attendees]
        
        # Create event
        result = google_client.calendar.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        return CreateEventResponse(
            ok=True,
            event_id=result.get('id'),
            event_link=result.get('htmlLink'),
            message="Event created successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to create event: {e}")
        return CreateEventResponse(
            ok=False,
            error_type="create_failed",
            message=str(e)
        )


@router.post("/list-events", response_model=ListEventsResponse)
async def list_events(request: ListEventsRequest) -> Dict[str, Any]:
    """
    List calendar events.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Listing events (max: {request.max_results})")
    
    if not google_client.is_authenticated():
        return ListEventsResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Build parameters
        params = {
            'calendarId': 'primary',
            'maxResults': request.max_results,
            'singleEvents': True,
            'orderBy': 'startTime'
        }
        
        if request.time_min:
            params['timeMin'] = request.time_min
        else:
            # Default to now
            params['timeMin'] = datetime.utcnow().isoformat() + 'Z'
        
        if request.time_max:
            params['timeMax'] = request.time_max
        
        # List events
        results = google_client.calendar.events().list(**params).execute()
        events = results.get('items', [])
        
        # Convert to summaries
        event_summaries = []
        for event in events:
            start = event.get('start', {})
            end = event.get('end', {})
            
            event_summaries.append(EventSummary(
                id=event['id'],
                summary=event.get('summary'),
                start=start.get('dateTime', start.get('date')),
                end=end.get('dateTime', end.get('date')),
                location=event.get('location')
            ))
        
        return ListEventsResponse(
            ok=True,
            events=event_summaries,
            message="Events retrieved successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to list events: {e}")
        return ListEventsResponse(
            ok=False,
            error_type="list_failed",
            message=str(e)
        )
