"""
Resume Parser Library

A Python library for extracting links and text content from PDF resumes.
Includes Firebase Firestore integration for storing extracted data.
"""

import pymupdf
import re
import json
import os
from firebase_config import save_resume_data


# Link Classification Patterns
GITHUB_PROFILE_PATTERN = r"https?://(?:www\.)?github\.com/([^/]+)/?$"
GITHUB_PROJECT_PATTERN = r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)"
LINKEDIN_PROFILE_PATTERN = r"https?://(?:www\.)?linkedin\.com/in/([^/]+)/?$"
EMAIL_PATTERN = r"mailto:([^?]+)"
PORTFOLIO_GITHUB_PATTERN = r"https?://([^/]+)\.github\.io/?"


def categorize_link(url):
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


def extract_resume_links(pdf_path):
    """
    Extract and categorize embedded links from a PDF resume.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary containing categorized links
    """
    resume = pymupdf.open(pdf_path)

    links_data = {
        "github": {"profile": [], "project": []},
        "linkedin": {"profile": []},
        "portfolio": [],
        "other": [],
    }

    for page_num in range(len(resume)):
        page = resume[page_num]
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
                else:
                    links_data["other"].append(cleaned_url)

    resume.close()
    return links_data


def extract_resume_text(pdf_path):
    """
    Extract all text content from a PDF resume.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: All text content from the PDF
    """
    resume = pymupdf.open(pdf_path)

    all_text = ""
    for page_num in range(len(resume)):
        page = resume[page_num]
        text = page.get_text()
        all_text += text + "\n"

    resume.close()
    return all_text


def process_resume(pdf_path):
    """
    Process resume and return structured data with links and raw text.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary containing links and text content
    """
    # Extract links
    links_data = extract_resume_links(pdf_path)

    # Extract raw text
    text_content = extract_resume_text(pdf_path)

    # Create final JSON structure
    resume_data = {"links": links_data, "metadata": {"text_content": text_content}}

    return resume_data


def process_resume_to_json(pdf_path):
    """
    Process resume and return JSON string.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: JSON string containing resume data
    """
    # Process resume
    resume_data = process_resume(pdf_path)

    # Convert to JSON string
    json_string = json.dumps(resume_data, indent=2)

    return json_string


def process_resume_with_firestore(pdf_path):
    """
    Process resume and save JSON data to Firestore.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary containing resume data with Firestore document ID
    """
    # Process resume using existing function
    resume_data = process_resume(pdf_path)

    # Get filename for Firestore
    filename = os.path.basename(pdf_path)

    try:
        # Save data to Firestore
        doc_id = save_resume_data(resume_data, filename)
        resume_data["document_id"] = doc_id
        print(f"✅ Data saved to Firestore with ID: {doc_id}")

    except Exception as e:
        print(f"❌ Firestore upload failed: {str(e)}")
        resume_data["firebase_error"] = str(e)

    return resume_data


def process_resume_to_json_with_firestore(pdf_path):
    """
    Process resume, save to Firestore, and return JSON string.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: JSON string containing resume data with Firestore document ID
    """
    # Process resume with Firestore
    resume_data = process_resume_with_firestore(pdf_path)

    # Convert to JSON string
    json_string = json.dumps(resume_data, indent=2)

    return json_string


# Example usage
if __name__ == "__main__":
    # Example: Process a resume
    pdf_file = "Test_Resumes/Sarthak_Resume.pdf"

    if os.path.exists(pdf_file):
        print("=== PROCESSING RESUME WITH FIRESTORE ===")

        # Process resume with Firestore only
        result = process_resume_with_firestore(pdf_file)

        # Display results
        print("\n=== EXTRACTED LINKS ===")
        flat_links = {}
        for category, data in result["links"].items():
            if isinstance(data, dict):
                for subcategory, urls in data.items():
                    if urls:
                        flat_links[f"{category}_{subcategory}"] = urls
            elif data:
                flat_links[category] = data

        for category, urls in flat_links.items():
            print(f"\n{category.upper()}:")
            for url in urls:
                print(f"  {url}")

        print(f"\n=== METADATA ===")
        text_content = result["metadata"]["text_content"]
        print(f"Text Content Length: {len(text_content)} characters")
        print(f"Text Preview (first 200 chars):")
        print(text_content[:200] + "..." if len(text_content) > 200 else text_content)

        # Show Firestore info
        if "document_id" in result:
            print(f"\n=== FIRESTORE ===")
            print(f"Document ID: {result['document_id']}")

        if "firebase_error" in result:
            print(f"Firebase Error: {result['firebase_error']}")

        # Show JSON result
        print(f"\n=== JSON RESULT ===")
        json_result = process_resume_to_json_with_firestore(pdf_file)
        print("JSON string length:", len(json_result))
        print("First 300 characters of JSON:")
        print(json_result[:300] + "...")
    else:
        print(f"File {pdf_file} not found!")


