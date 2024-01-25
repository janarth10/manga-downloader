import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# https://developers.google.com/drive/api/quickstart/python
# CREDENTIALS_PATH = '/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/configs/credentials.json'
CREDENTIALS_PATH = '/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/configs/manga-oauth-2024-01.json'
TOKEN_PATH = '/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/configs/token.json'

def get_google_drive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            # creds = flow.run_local_server(    
            #     host='localhost',
            #     port=56655
            # )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return None
    

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
