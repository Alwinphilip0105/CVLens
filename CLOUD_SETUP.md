# Cloud Integration Setup Guide

This guide will help you set up Google Drive and Firebase integration for your Streamlit resume analysis app.

## Prerequisites

1. **Google Cloud Project** with Drive API and Firebase enabled
2. **Firebase Project** with Firestore database
3. **Service Account** credentials for both services

## Step 1: Install Dependencies

```bash
pip install -r requirements_cloud.txt
```

## Step 2: Google Drive Setup

### 2.1 Enable Google Drive API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "APIs & Services" > "Library"
4. Search for "Google Drive API" and enable it

### 2.2 Create OAuth Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the JSON file and save as `Resume_Parser/gdrive_credentials.json`

## Step 3: Firebase Setup

### 3.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable Firestore Database

### 3.2 Create Service Account
1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Download the JSON file and save as `Resume_Parser/firebase-service-account.json`

## Step 4: File Structure

Your project should have this structure:
```
RU_HACK-1/
├── Resume_Parser/
│   ├── gdrive_credentials.json      # Google Drive OAuth credentials
│   ├── firebase-service-account.json # Firebase service account
│   ├── resume_parser.py
│   ├── gdrive_config.py
│   └── firebase_config.py
├── Frontend/
│   ├── utils/
│   │   └── cloud_integration.py
│   └── streamlit_app.py
└── requirements_cloud.txt
```

## Step 5: Test the Integration

1. Run your Streamlit app:
   ```bash
   streamlit run Frontend/streamlit_app.py
   ```

2. Upload a resume PDF
3. Check the "☁️ Cloud Integration Status" expander
4. You should see "Cloud integration available!" if setup is correct

## Features

### Automatic Resume Upload
- When you upload a PDF resume, it's automatically uploaded to Google Drive
- The PDF is stored in a "Resume PDFs" folder
- You get a shareable Google Drive link

### Firebase Data Storage
- Resume text and extracted links are saved to Firestore
- Complete user profile (form data + resume) can be saved
- Data is organized in collections: `resumes` and `user_profiles`

### Cloud Status Display
- Shows if cloud services are available
- Displays Google Drive and Firebase status
- Provides helpful error messages if setup is incomplete

## Troubleshooting

### Common Issues

1. **"Cloud integration not available"**
   - Check if all dependencies are installed
   - Verify credential files are in the correct location
   - Check file permissions

2. **"Failed to initialize cloud services"**
   - Verify Firebase service account JSON is valid
   - Check if Firestore is enabled in Firebase Console
   - Ensure project ID matches in service account

3. **"Google Drive upload failed"**
   - Run the app once to complete OAuth flow
   - Check if Drive API is enabled
   - Verify OAuth credentials are correct

### Testing Individual Components

You can test the cloud integration separately:

```python
# Test cloud integration
from Frontend.utils.cloud_integration import test_cloud_integration
test_cloud_integration()
```

## Security Notes

- Never commit credential files to version control
- Add `*.json` to your `.gitignore` file
- Use environment variables for production deployments
- Regularly rotate service account keys

## Production Deployment

For production deployment:

1. Use environment variables instead of JSON files
2. Set up proper IAM roles and permissions
3. Enable audit logging
4. Use Firebase Security Rules for data access control
5. Consider using Google Cloud Secret Manager

## Support

If you encounter issues:
1. Check the console output for detailed error messages
2. Verify all credential files are properly formatted
3. Ensure all APIs are enabled in Google Cloud Console
4. Check Firebase project settings and permissions
