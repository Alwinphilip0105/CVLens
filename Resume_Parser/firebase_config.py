import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import json


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    # Check if Firebase is already initialized
    try:
        # Try to get the default app
        app = firebase_admin.get_app()
        # If we get here, Firebase is already initialized
        db = firestore.client()
        bucket = storage.bucket()
        return db, bucket
    except ValueError:
        # Firebase is not initialized, so initialize it
        pass

    # Path to your service account key
    # Get the directory where this file is located (Resume_Parser)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(current_dir, "firebase-service-account.json")

    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Service account key not found at {cred_path}")

    # Load the service account JSON to extract project ID
    with open(cred_path, "r") as f:
        service_account = json.load(f)

    project_id = service_account.get("project_id")
    if not project_id:
        raise ValueError("Project ID not found in service account JSON")

    # Initialize Firebase Admin
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(
        cred,
        {"storageBucket": f"{project_id}.appspot.com"},
    )

    # Initialize Firestore and Storage
    db = firestore.client()
    bucket = storage.bucket()

    return db, bucket


def save_resume_data(resume_data, filename):
    """Save resume data to Firestore (JSON only)"""
    print("\n" + "="*80)
    print("🔥 DEBUGGING: Firestore Save Operation")
    print("="*80)
    print(f"📁 Filename: {filename}")
    print(f"📄 Document ID: {filename.replace('.pdf', '')}")
    print("📊 Resume data being saved to Firestore:")
    print(json.dumps(resume_data, indent=2, default=str))
    print("="*80)
    
    try:
        db, bucket = initialize_firebase()
        print("✅ Firebase initialized successfully")

        # Save to Firestore
        doc_id = filename.replace(".pdf", "")
        doc_ref = db.collection("resumes").document(doc_id)
        
        print(f"🔄 Saving to collection 'resumes' with document ID: {doc_id}")
        doc_ref.set(resume_data)
        
        print(f"✅ Successfully saved to Firestore with ID: {doc_ref.id}")
        print("="*80)

        return doc_ref.id
        
    except Exception as e:
        print(f"❌ Firestore save failed: {str(e)}")
        import traceback
        print(f"Full error traceback: {traceback.format_exc()}")
        print("="*80)
        return None

def list_firebase_documents():
    """
    List all documents in the resumes collection.
    """
    try:
        db, bucket = initialize_firebase()
        
        # Get all documents from the resumes collection
        docs = db.collection("resumes").stream()
        
        documents = []
        for doc in docs:
            documents.append({
                "id": doc.id,
                "data": doc.to_dict()
            })
        
        return documents
    except Exception as e:
        print(f"Error listing Firebase documents: {e}")
        return []
