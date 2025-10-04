"""
Resume Parser Package

A Python package for extracting links and text content from PDF resumes.
"""

from .resume_parser import (
    categorize_link,
    extract_resume_links,
    extract_resume_text,
    process_resume,
    process_resume_to_json,
)

__version__ = "1.0.0"
__author__ = "Sarthak Chandervanshi"

__all__ = [
    "categorize_link",
    "extract_resume_links",
    "extract_resume_text",
    "process_resume",
    "process_resume_to_json",
]
