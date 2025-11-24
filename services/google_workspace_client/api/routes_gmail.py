"""Gmail API routes"""
import logging
import base64
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..models.schemas import (
    SendEmailRequest,
    SendEmailResponse,
    ListEmailsRequest,
    ListEmailsResponse,
    EmailSummary
)
from ..core.google_client import google_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/google/gmail", tags=["gmail"])


@router.post("/send", response_model=SendEmailResponse)
async def send_email(request: SendEmailRequest) -> Dict[str, Any]:
    """
    Send an email via Gmail.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Sending email to: {request.to}")
    
    if not google_client.is_authenticated():
        return SendEmailResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # Create message
        message = MIMEText(request.body, 'html' if request.is_html else 'plain')
        message['to'] = ', '.join(request.to)
        message['subject'] = request.subject
        
        if request.cc:
            message['cc'] = ', '.join(request.cc)
        if request.bcc:
            message['bcc'] = ', '.join(request.bcc)
        
        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Send via Gmail API
        result = google_client.gmail.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        return SendEmailResponse(
            ok=True,
            message_id=result.get('id'),
            message="Email sent successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return SendEmailResponse(
            ok=False,
            error_type="send_failed",
            message=str(e)
        )


@router.post("/list", response_model=ListEmailsResponse)
async def list_emails(request: ListEmailsRequest) -> Dict[str, Any]:
    """
    List emails from Gmail.
    
    Returns a standardized response with 'ok' field.
    """
    logger.info(f"Listing emails (max: {request.max_results})")
    
    if not google_client.is_authenticated():
        return ListEmailsResponse(
            ok=False,
            error_type="not_authenticated",
            message="Google authentication required"
        )
    
    try:
        # List messages
        params = {
            'userId': 'me',
            'maxResults': request.max_results
        }
        
        if request.query:
            params['q'] = request.query
        
        results = google_client.gmail.users().messages().list(**params).execute()
        messages = results.get('messages', [])
        
        # Get details for each message
        email_summaries = []
        for msg in messages:
            msg_detail = google_client.gmail.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Subject', 'From', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg_detail.get('payload', {}).get('headers', [])}
            
            email_summaries.append(EmailSummary(
                id=msg['id'],
                thread_id=msg.get('threadId'),
                subject=headers.get('Subject'),
                from_email=headers.get('From'),
                date=headers.get('Date'),
                snippet=msg_detail.get('snippet')
            ))
        
        return ListEmailsResponse(
            ok=True,
            emails=email_summaries,
            total=len(email_summaries),
            message="Emails retrieved successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to list emails: {e}")
        return ListEmailsResponse(
            ok=False,
            error_type="list_failed",
            message=str(e)
        )
