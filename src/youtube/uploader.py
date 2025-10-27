"""
YouTube API Integration for uploading videos
"""
import os
import logging
import pickle
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class YouTubeUploader:
    """Handles uploading videos to YouTube Shorts"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, client_secrets_file: str = "client_secrets.json",
                 token_file: str = "token.pickle"):
        """
        Initialize YouTube uploader
        
        Args:
            client_secrets_file: Path to OAuth client secrets JSON file
            token_file: Path to save/load authentication token
        """
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.logger = logging.getLogger(__name__)
        self.youtube = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with YouTube API using OAuth
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            creds = None
            
            # Load existing credentials
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    self.logger.info("Refreshing expired credentials")
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.client_secrets_file):
                        self.logger.error(f"Client secrets file not found: {self.client_secrets_file}")
                        self.logger.info("Please download from Google Cloud Console: https://console.cloud.google.com/")
                        return False
                    
                    self.logger.info("Starting OAuth flow")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            # Build YouTube service
            self.youtube = build('youtube', 'v3', credentials=creds)
            self.logger.info("Successfully authenticated with YouTube API")
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return False
    
    def upload_video(self, video_path: str, title: str, description: str = "",
                    category: str = "17", privacy_status: str = "public",
                    tags: Optional[list] = None) -> Optional[str]:
        """
        Upload video to YouTube as a Short
        
        Args:
            video_path: Path to video file to upload
            title: Video title (max 100 chars for Shorts)
            description: Video description
            category: YouTube category ID (17 = Sports)
            privacy_status: Privacy setting (public, private, unlisted)
            tags: List of tags for the video
            
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        try:
            # Ensure title is appropriate for Shorts
            if len(title) > 100:
                title = title[:97] + "..."
            
            # Add #Shorts to description for YouTube Shorts
            if "#Shorts" not in description and "#shorts" not in description:
                description = f"{description}\n\n#Shorts #Sports #AI"
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or ['Sports', 'AI', 'Commentary', 'Shorts'],
                    'categoryId': category
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create MediaFileUpload object
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # Upload in a single request
                resumable=True,
                mimetype='video/mp4'
            )
            
            self.logger.info(f"Uploading video: {title}")
            
            # Execute upload
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    self.logger.info(f"Upload progress: {progress}%")
            
            video_id = response['id']
            self.logger.info(f"Successfully uploaded! Video ID: {video_id}")
            self.logger.info(f"Video URL: https://www.youtube.com/shorts/{video_id}")
            
            return video_id
            
        except HttpError as e:
            self.logger.error(f"HTTP error during upload: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error uploading video: {e}")
            return None
    
    def get_upload_status(self, video_id: str) -> Optional[dict]:
        """
        Get the processing status of an uploaded video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Status dictionary or None if error
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        try:
            request = self.youtube.videos().list(
                part='status,processingDetails',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting upload status: {e}")
            return None
