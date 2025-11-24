"""Google API Client - handles authentication and API calls"""
import os
import pickle
import logging
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..config import settings

logger = logging.getLogger(__name__)


class GoogleWorkspaceClient:
    """
    Client for Google Workspace APIs.
    
    Handles OAuth authentication and provides access to:
    - Gmail
    - Calendar  
    - Drive
    - Sheets
    - Docs
    - Tasks
    """
    
    def __init__(self):
        self.creds: Optional[Credentials] = None
        self._services = {}
        self._init_credentials()
    
    def _init_credentials(self):
        """Initialize Google OAuth credentials"""
        token_path = settings.google_token_file
        creds_path = settings.google_credentials_file
        
        # Load existing token if available
        if os.path.exists(token_path):
            try:
                with open(token_path, 'rb') as token:
                    self.creds = pickle.load(token)
                logger.info("Loaded existing Google credentials")
            except Exception as e:
                logger.error(f"Failed to load token: {e}")
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    logger.info("Refreshed Google credentials")
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    self.creds = None
            
            # If still no valid creds, need OAuth flow
            if not self.creds:
                if os.path.exists(creds_path):
                    logger.warning("No valid credentials. OAuth flow required.")
                    logger.warning(f"Run: python -m services.google_workspace_client.auth")
                else:
                    logger.error(f"Credentials file not found: {creds_path}")
            
            # Save the credentials
            if self.creds:
                try:
                    with open(token_path, 'wb') as token:
                        pickle.dump(self.creds, token)
                    logger.info("Saved Google credentials")
                except Exception as e:
                    logger.error(f"Failed to save token: {e}")
    
    def _get_service(self, service_name: str, version: str):
        """Get or create a Google API service"""
        key = f"{service_name}_{version}"
        
        if key not in self._services:
            if not self.creds or not self.creds.valid:
                raise Exception("Google credentials not initialized")
            
            self._services[key] = build(service_name, version, credentials=self.creds)
            logger.info(f"Created {service_name} service")
        
        return self._services[key]
    
    @property
    def gmail(self):
        """Get Gmail API service"""
        return self._get_service('gmail', 'v1')
    
    @property
    def calendar(self):
        """Get Calendar API service"""
        return self._get_service('calendar', 'v3')
    
    @property
    def drive(self):
        """Get Drive API service"""
        return self._get_service('drive', 'v3')
    
    @property
    def sheets(self):
        """Get Sheets API service"""
        return self._get_service('sheets', 'v4')
    
    @property
    def docs(self):
        """Get Docs API service"""
        return self._get_service('docs', 'v1')
    
    @property
    def tasks(self):
        """Get Tasks API service"""
        return self._get_service('tasks', 'v1')
    
    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return self.creds is not None and self.creds.valid


# Global client instance
google_client = GoogleWorkspaceClient()
