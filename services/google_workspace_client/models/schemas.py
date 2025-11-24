"""Pydantic models for request/response schemas"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any


# ============================================================================
# Base Response Model
# ============================================================================

class BaseResponse(BaseModel):
    """Base response model - all responses inherit from this"""
    ok: bool = Field(..., description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Human-readable message")
    error_type: Optional[str] = Field(None, description="Error type if ok=False")


# ============================================================================
# Gmail Models
# ============================================================================

class SendEmailRequest(BaseModel):
    """Request to send an email"""
    to: List[EmailStr] = Field(..., description="Recipient email addresses")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body (plain text or HTML)")
    cc: Optional[List[EmailStr]] = Field(None, description="CC recipients")
    bcc: Optional[List[EmailStr]] = Field(None, description="BCC recipients")
    is_html: bool = Field(default=False, description="Whether body is HTML")


class SendEmailResponse(BaseResponse):
    """Response for sending an email"""
    message_id: Optional[str] = Field(None, description="Gmail message ID")


class ListEmailsRequest(BaseModel):
    """Request to list emails"""
    max_results: int = Field(default=10, description="Maximum number of emails")
    query: Optional[str] = Field(None, description="Gmail search query")


class EmailSummary(BaseModel):
    """Summary of an email"""
    id: str
    thread_id: str
    subject: Optional[str] = None
    from_email: Optional[str] = None
    date: Optional[str] = None
    snippet: Optional[str] = None


class ListEmailsResponse(BaseResponse):
    """Response for listing emails"""
    emails: Optional[List[EmailSummary]] = Field(None, description="List of emails")
    total: Optional[int] = Field(None, description="Total number of emails")


# ============================================================================
# Calendar Models
# ============================================================================

class CreateEventRequest(BaseModel):
    """Request to create a calendar event"""
    summary: str = Field(..., description="Event title")
    start_time: str = Field(..., description="Start time (ISO 8601)")
    end_time: str = Field(..., description="End time (ISO 8601)")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Event location")
    attendees: Optional[List[EmailStr]] = Field(None, description="Attendee emails")


class CreateEventResponse(BaseResponse):
    """Response for creating an event"""
    event_id: Optional[str] = Field(None, description="Calendar event ID")
    event_link: Optional[str] = Field(None, description="Event link")


class ListEventsRequest(BaseModel):
    """Request to list calendar events"""
    max_results: int = Field(default=10, description="Maximum number of events")
    time_min: Optional[str] = Field(None, description="Minimum time (ISO 8601)")
    time_max: Optional[str] = Field(None, description="Maximum time (ISO 8601)")


class EventSummary(BaseModel):
    """Summary of a calendar event"""
    id: str
    summary: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    location: Optional[str] = None


class ListEventsResponse(BaseResponse):
    """Response for listing events"""
    events: Optional[List[EventSummary]] = Field(None, description="List of events")


# ============================================================================
# Drive Models
# ============================================================================

class SearchDriveRequest(BaseModel):
    """Request to search Google Drive"""
    query: str = Field(..., description="Search query")
    max_results: int = Field(default=10, description="Maximum number of results")


class DriveFile(BaseModel):
    """Drive file summary"""
    id: str
    name: str
    mime_type: Optional[str] = None
    web_view_link: Optional[str] = None
    created_time: Optional[str] = None


class SearchDriveResponse(BaseResponse):
    """Response for Drive search"""
    files: Optional[List[DriveFile]] = Field(None, description="List of files")


# ============================================================================
# Sheets Models
# ============================================================================

class CreateSheetRequest(BaseModel):
    """Request to create a spreadsheet"""
    title: str = Field(..., description="Spreadsheet title")


class CreateSheetResponse(BaseResponse):
    """Response for creating a spreadsheet"""
    spreadsheet_id: Optional[str] = Field(None, description="Spreadsheet ID")
    spreadsheet_url: Optional[str] = Field(None, description="Spreadsheet URL")


class ReadSheetRequest(BaseModel):
    """Request to read from a spreadsheet"""
    spreadsheet_id: str = Field(..., description="Spreadsheet ID")
    range: str = Field(default="Sheet1", description="Range to read")


class ReadSheetResponse(BaseResponse):
    """Response for reading a spreadsheet"""
    values: Optional[List[List[Any]]] = Field(None, description="Cell values")


# ============================================================================
# Docs Models
# ============================================================================

class CreateDocRequest(BaseModel):
    """Request to create a document"""
    title: str = Field(..., description="Document title")


class CreateDocResponse(BaseResponse):
    """Response for creating a document"""
    document_id: Optional[str] = Field(None, description="Document ID")
    document_url: Optional[str] = Field(None, description="Document URL")


# ============================================================================
# Tasks Models
# ============================================================================

class CreateTaskRequest(BaseModel):
    """Request to create a task"""
    title: str = Field(..., description="Task title")
    notes: Optional[str] = Field(None, description="Task notes")
    due: Optional[str] = Field(None, description="Due date (ISO 8601)")


class CreateTaskResponse(BaseResponse):
    """Response for creating a task"""
    task_id: Optional[str] = Field(None, description="Task ID")
