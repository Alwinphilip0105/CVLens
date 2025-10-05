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
    """Authenticate with Google Drive API using Service Account"""
    # Path to your service account credentials
    cred_path = os.path.join(
        os.path.dirname(__file__), "gdrive-service-account.json"
    )

    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Google Drive service account credentials not found at {cred_path}"
        )

    # Use service account credentials
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=SCOPES
    )

    return build("drive", "v3", credentials=creds)


def upload_pdf_to_gdrive(file_path, filename, folder_name="Resume PDFs"):
    """Upload PDF to Google Drive"""
    try:
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
    except FileNotFoundError as e:
        print(f"Google Drive credentials not found: {e}")
        return None, None
    except Exception as e:
        print(f"Google Drive upload failed: {e}")
        return None, None


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
    except FileNotFoundError as e:
        print(f"Google Drive credentials not found: {e}")
        return []
    except Exception as e:
        print(f"Error listing Google Drive files: {e}")
        return []