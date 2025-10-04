import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes for Google Drive API
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def authenticate_gdrive():
    """Authenticate with Google Drive API using OAuth"""
    creds = None

    # Check if token.pickle exists (stored credentials)
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Path to your OAuth credentials
            cred_path = os.path.join(
                os.path.dirname(__file__), "gdrive_credentials.json"
            )

            if not os.path.exists(cred_path):
                raise FileNotFoundError(
                    f"Google Drive credentials not found at {cred_path}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


def upload_pdf_to_gdrive(file_path, filename, folder_name="Resume PDFs"):
    """Upload PDF to Google Drive"""
    service = authenticate_gdrive()

    # Create folder if it doesn't exist
    folder_id = create_folder_if_not_exists(service, folder_name)

    # Upload file
    file_metadata = {"name": filename, "parents": [folder_id]}

    media = MediaFileUpload(file_path, mimetype="application/pdf")
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id,webViewLink")
        .execute()
    )

    return file.get("webViewLink"), file.get("id")


def create_folder_if_not_exists(service, folder_name):
    """Create folder if it doesn't exist, return folder ID"""
    # Check if folder exists
    results = (
        service.files()
        .list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)",
        )
        .execute()
    )

    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]
    else:
        # Create folder
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        folder = service.files().create(body=folder_metadata, fields="id").execute()
        return folder.get("id")

def list_gdrive_files():
    """
    List all files in the Resume PDFs folder.
    """
    try:
        service = authenticate_gdrive()
        folder_id = create_folder_if_not_exists(service, "Resume PDFs")
        
        # Query files in the folder
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id,name,createdTime,size)").execute()
        files = results.get("files", [])
        
        return files
    except Exception as e:
        print(f"Error listing Google Drive files: {e}")
        return []