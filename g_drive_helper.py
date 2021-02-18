from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = 'configs/token.pickle'
CREDS_PATH = 'configs/google_api_credentials.json'

def get_google_drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(drive_file_name, file_path, parents=[]):
    service = get_google_drive_service()

    file_metadata = {
        'name': drive_file_name,
        'parents': parents,
    }
    media = MediaFileUpload(file_path)
    file_resource = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name,webViewLink,webContentLink'
    ).execute()
    return file_resource

# not being used anymore bc we can get these links on creation
def get_drive_download_and_view_links(service, drive_file_id):
    file_resource = service.files().get(
        fileId=drive_file_id,
        fields='id,name,webViewLink,webContentLink'
    ).execute()
    return file_resource
