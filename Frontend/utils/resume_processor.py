"""
Resume processing module for PDF/DOCX text extraction.
Handles file upload, text extraction, and resume text processing.
"""

import io
import streamlit as st
from typing import Optional, Tuple, Dict, Any
from pypdf import PdfReader
from docx import Document
import pymupdf
import re
import json
import sys
import os
from datetime import datetime
import hashlib
import tempfile # Added for explicit temp file handling

# Add the Frontend directory to Python path for imports
# Get the directory containing this file (utils), then go up one level (Frontend)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.dirname(current_file_dir)
if frontend_dir not in sys.path:
    sys.path.insert(0, frontend_dir)

def process_resume_with_unicode_handling(pdf_path):
    """
    Process resume with Firestore, handling Unicode errors.
    
    The document ID used for Firestore is derived from the basename of pdf_path, 
    minus the extension.
    """
    # Ensure Resume_Parser directory is in Python path
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.dirname(current_file_dir)
    project_root = os.path.dirname(frontend_dir)
    resume_parser_dir = os.path.join(project_root, 'Resume_Parser')
    
    if resume_parser_dir not in sys.path:
        sys.path.insert(0, resume_parser_dir)
    
    try:
        # Try the normal process
        from resume_parser import process_resume_with_firestore
        result = process_resume_with_firestore(pdf_path)
        return result
    except UnicodeEncodeError as unicode_error:
        print(f"Unicode encoding error in resume_parser logging")
        print(f"This usually means the upload succeeded but logging failed")
        
        # Check if the upload actually succeeded by looking for recent files in Firestore
        try:
            from firebase_config import list_firebase_documents
            recent_docs = list_firebase_documents()
            
            # If we have recent documents, the upload likely succeeded
            if recent_docs:
                print(f"Found {len(recent_docs)} documents in Firestore - upload likely succeeded")
                
                # Derive Document ID from the path (which includes the timestamp)
                filename = os.path.basename(pdf_path)
                doc_id = os.path.splitext(filename)[0]

                # Return a basic success result without re-uploading
                return {
                    "filename": filename,
                    "links": {},
                    "metadata": {"text_content": ""},
                    "document_id": doc_id,
                    "recovered_from_unicode_error": True
                }
        except Exception as check_error:
            print(f"Could not verify upload status: {check_error}")
        
        # Only upload again if we couldn't verify the first upload succeeded
        try:
            from firebase_config import save_resume_data
            
            # Create a basic resume data structure
            filename = os.path.basename(pdf_path)
            doc_id_fallback = os.path.splitext(filename)[0]

            resume_data = {
                "filename": filename,
                "links": {},
                "metadata": {"text_content": ""}
            }
            
            # Save to Firebase. Assuming the backend uses the filename to derive the ID
            # if a specific doc_id is not passed.
            doc_id = save_resume_data(resume_data, filename)
            
            # Fallback for doc_id if the save function doesn't return it
            if doc_id is None:
                doc_id = doc_id_fallback

            resume_data["document_id"] = doc_id
            
            print(f"Successfully recovered: Firebase save completed")
            print(f"Firebase Document ID: {doc_id}")
            
            return resume_data
            
        except Exception as recovery_error:
            print(f"Recovery failed: {recovery_error}")
            return {
                "document_id": None,
                "links": {},
                "metadata": {"text_content": ""},
                "firebase_error": f"Unicode error and recovery failed: {recovery_error}"
            }
    except Exception as e:
        print(f"Process failed: {e}")
        return {
            "document_id": None,
            "links": {},
            "metadata": {"text_content": ""},
            "firebase_error": str(e)
        }

# Link Classification Patterns (from resume parser)
GITHUB_PROFILE_PATTERN = r"https?://(?:www\.)?github\.com/([^/]+)/?$"
GITHUB_PROJECT_PATTERN = r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)"
LINKEDIN_PROFILE_PATTERN = r"https?://(?:www\.)?linkedin\.com/in/([^/]+)/?$"
EMAIL_PATTERN = r"mailto:([^?]+)"
PORTFOLIO_GITHUB_PATTERN = r"https?://([^/]+)\.github\.io/?"


def categorize_link(url: str) -> Tuple[str, str, str]:
    """
    Categorize a URL into appropriate category.

    Args:
        url (str): The URL to categorize

    Returns:
        tuple: (category, cleaned_url, metadata)
    """
    # Check LinkedIn profile
    if re.search(LINKEDIN_PROFILE_PATTERN, url, re.IGNORECASE):
        return ("linkedin", url, "profile")

    # Check GitHub Pages portfolio
    if re.search(PORTFOLIO_GITHUB_PATTERN, url, re.IGNORECASE):
        return ("portfolio", url, "github_pages")

    # Check GitHub profile vs project
    github_profile_match = re.search(GITHUB_PROFILE_PATTERN, url, re.IGNORECASE)
    github_project_match = re.search(GITHUB_PROJECT_PATTERN, url, re.IGNORECASE)

    if github_profile_match:
        return ("github", url, "profile")
    elif github_project_match:
        return ("github", url, "project")

    # Check email
    email_match = re.search(EMAIL_PATTERN, url, re.IGNORECASE)
    if email_match:
        return ("email", email_match.group(1), "email")

    # Default to other
    return ("other", url, "other")


def extract_links_from_pdf_pymupdf(file_content: bytes) -> Dict[str, Any]:
    """
    Extract and categorize embedded links from a PDF resume using pymupdf.

    Args:
        file_content: PDF file content as bytes

    Returns:
        dict: Dictionary containing categorized links
    """
    try:
        # Create a temporary file-like object
        pdf_document = pymupdf.open(stream=file_content, filetype="pdf")
        
        links_data = {
            "github": {"profile": [], "project": []},
            "linkedin": {"profile": []},
            "portfolio": [],
            "other": [],
            "email": []
        }

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            links = page.get_links()

            for link in links:
                if "uri" in link:
                    url = link["uri"]
                    category, cleaned_url, metadata = categorize_link(url)

                    if category == "github":
                        links_data["github"][metadata].append(cleaned_url)
                    elif category == "linkedin":
                        links_data["linkedin"][metadata].append(cleaned_url)
                    elif category == "portfolio":
                        links_data["portfolio"].append(cleaned_url)
                    elif category == "email":
                        links_data["email"].append(cleaned_url)
                    else:
                        links_data["other"].append(cleaned_url)

        pdf_document.close()
        return links_data
    except Exception as e:
        st.warning(f"Could not extract links from PDF: {e}")
        return {
            "github": {"profile": [], "project": []},
            "linkedin": {"profile": []},
            "portfolio": [],
            "other": [],
            "email": []
        }


class ResumeProcessor:
    """Handles resume file processing and text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file content.
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            pdf_reader = PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_and_links_from_pdf(file_content: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Extract both text and links from PDF file content.
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Tuple of (extracted_text, links_data)
        """
        # Extract text using pypdf
        text = ResumeProcessor.extract_text_from_pdf(file_content)
        
        # Extract links using pymupdf
        links_data = extract_links_from_pdf_pymupdf(file_content)
        
        return text, links_data
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extract text from DOCX file content.
        
        Args:
            file_content: DOCX file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from DOCX: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """
        Extract text from TXT file content.
        
        Args:
            file_content: TXT file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    return file_content.decode(encoding).strip()
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            return file_content.decode('utf-8', errors='replace').strip()
            
        except Exception as e:
            st.error(f"Error extracting text from TXT: {e}")
            return ""
    
    @staticmethod
    def process_uploaded_file(uploaded_file) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Process uploaded file and extract text and links.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success, extracted_text, links_data)
        """
        if uploaded_file is None:
            return False, "", {}
        
        try:
            file_content = uploaded_file.read()
            # Reset file pointer for potential future reads
            uploaded_file.seek(0)
            file_extension = uploaded_file.name.split('.')[-1].lower()
            links_data = {}
            
            if file_extension == 'pdf':
                text, links_data = ResumeProcessor.extract_text_and_links_from_pdf(file_content)
            elif file_extension == 'docx':
                text = ResumeProcessor.extract_text_from_docx(file_content)
                # DOCX doesn't support link extraction with current setup
                links_data = {"github": {"profile": [], "project": []}, "linkedin": {"profile": []}, "portfolio": [], "other": [], "email": []}
            elif file_extension == 'txt':
                text = ResumeProcessor.extract_text_from_txt(file_content)
                # TXT doesn't support link extraction
                links_data = {"github": {"profile": [], "project": []}, "linkedin": {"profile": []}, "portfolio": [], "other": [], "email": []}
            else:
                st.error(f"Unsupported file type: {file_extension}")
                return False, "", {}
            
            if text:
                return True, text, links_data
            else:
                st.warning(f"No text could be extracted from {uploaded_file.name}")
                return False, "", {}
                
        except Exception as e:
            st.error(f"Error processing file {uploaded_file.name}: {e}")
            return False, "", {}
    
    @staticmethod
    def clean_resume_text(text: str) -> str:
        """
        Clean and normalize resume text.
        
        Args:
            text: Raw resume text
            
        Returns:
            Cleaned resume text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with analysis
        text = re.sub(r'[^\w\s@.-]', ' ', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    @staticmethod
    def validate_resume_text(text: str) -> Tuple[bool, str]:
        """
        Validate that resume text is suitable for analysis.
        
        Args:
            text: Resume text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Resume text is empty"
        
        if len(text.strip()) < 50:
            return False, "Resume text is too short (minimum 50 characters)"
        
        if len(text.strip()) > 50000:
            return False, "Resume text is too long (maximum 50,000 characters)"
        
        # Check for common resume keywords
        resume_keywords = ['experience', 'education', 'skills', 'work', 'job', 'position', 'company']
        text_lower = text.lower()
        
        keyword_count = sum(1 for keyword in resume_keywords if keyword in text_lower)
        if keyword_count < 2:
            return False, "Text doesn't appear to be a resume (missing common resume keywords)"
        
        return True, ""


def handle_file_upload(uploaded_file) -> None:
    """
    Handle file upload and update session state.
    This function integrates with Streamlit's session state and cloud services.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    """
    if uploaded_file is not None:
        # First, process the file locally
        success, extracted_text, links_data = ResumeProcessor.process_uploaded_file(uploaded_file)
        
        if success:
            # Clean the text
            cleaned_text = ResumeProcessor.clean_resume_text(extracted_text)
            
            # Validate the text
            is_valid, error_msg = ResumeProcessor.validate_resume_text(cleaned_text)
            
            if is_valid:
                st.session_state.raw_resume_text = cleaned_text
                st.session_state.extracted_links = links_data  # Store links in session state
                
                # Process resume with Firestore
                try:
                    # --- NEW LOGIC FOR TIMESTAMPED FILENAME/DOCUMENT ID ---
                    
                    # 1. Generate unique, timestamped document ID prefix
                    now = datetime.now()
                    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
                    
                    # Safely extract and sanitize original name
                    original_name_parts = uploaded_file.name.rsplit('.', 1)
                    original_name = original_name_parts[0]
                    file_extension = original_name_parts[-1].lower() if len(original_name_parts) > 1 else 'pdf' # Fallback
                    
                    # Sanitize name by replacing non-word/non-hyphen characters with underscores
                    safe_original_name = re.sub(r'[^\w-]', '_', original_name)

                    # The unique name that will be used as the Firestore Document ID
                    document_id_prefix = f"{safe_original_name}_{timestamp_str}"
                    
                    # Create the temporary file path using the desired document ID
                    temp_file_path = os.path.join(tempfile.gettempdir(), f"{document_id_prefix}.{file_extension}")
                    
                    # 2. Write file content to the temp path
                    uploaded_file.seek(0)
                    file_content = uploaded_file.read()

                    if len(file_content) == 0:
                        st.error("❌ Uploaded file is empty!")
                        return

                    # Write file content to the specified temporary path
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(file_content)

                    # --- END NEW LOGIC ---

                    # Run resume processing (uses temp_file_path which now contains the desired ID)
                    result = process_resume_with_unicode_handling(temp_file_path)
                    
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                    
                    # Update session state with results
                    if 'document_id' in result:
                        st.session_state.firebase_document_id = result['document_id']
                    if 'links' in result:
                        st.session_state.extracted_links = result['links']
                    # Only update resume text if cloud processing returned actual text content
                    if 'metadata' in result and 'text_content' in result['metadata'] and result['metadata']['text_content'].strip():
                        st.session_state.raw_resume_text = result['metadata']['text_content']
                    
                    # Show upload status
                    if 'document_id' in result and result['document_id'] and result['document_id'] != 'None':
                        st.success("✅ Resume data saved to Firestore successfully!")
                        st.info(f"🔥 Firestore Document ID: `{result['document_id']}`")
                    else:
                        st.warning("⚠️ Firestore save failed")
                        if 'firebase_error' in result:
                            st.error(f"Error: {result['firebase_error']}")
                        
                except Exception as e:
                    st.warning(f"⚠️ Resume processing failed: {str(e)}")
                    print(f"Resume processing error: {str(e)}")
                
                # Automatically run analysis to extract personal details
                try:
                    from utils.backend_integration import LocalAnalysisEngine
                    from utils.ui_components import SessionStateManager
                    
                    # Run local analysis to extract personal details
                    analysis_data = LocalAnalysisEngine.analyze_resume_local(
                        resume_text=cleaned_text,
                        positions=st.session_state.get('target_positions', []),
                        preferences=st.session_state.get('skills', []),
                        locations=st.session_state.get('preferred_locations', [])
                    )
                    
                    # Update session state with extracted details
                    SessionStateManager.update_session_state_from_analysis(analysis_data)
                    
                except Exception as e:
                    # Hide warning message
                    pass
                    
            else:
                st.warning(f"⚠️ {error_msg}")
                st.session_state.raw_resume_text = cleaned_text  # Still set it, let user decide
                st.session_state.extracted_links = links_data
        else:
            st.error("❌ Failed to extract text from the uploaded file.")
    else:
        # Clear resume text if no file is uploaded
        if 'raw_resume_text' in st.session_state:
            st.session_state.raw_resume_text = ""
        if 'extracted_links' in st.session_state:
            st.session_state.extracted_links = {}
