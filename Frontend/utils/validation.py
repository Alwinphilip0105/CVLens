"""
Validation module for form validation logic.
Handles validation of required fields, max counts, and data integrity.
"""

import streamlit as st
import re
from typing import List, Dict, Any, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class FormValidator:
    """Handles form validation for the Streamlit app."""
    
    # Constants for validation limits
    MAX_LOCATIONS = 6
    MAX_POSITIONS = 5
    MAX_PREFERENCES = 10
    
    # Required fields
    REQUIRED_FIELDS = {
        'resume_text': 'Resume text',
        'preferred_locations': 'Preferred locations',
        'skills': 'Skills'
    }
    
    @staticmethod
    def validate_required_fields(session_state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that all required fields are filled.
        
        Args:
            session_state: Streamlit session state dictionary
            
        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        # Check resume text
        if not session_state.get('raw_resume_text', '').strip():
            missing_fields.append('Resume text')
        
        # Check preferred locations
        if not session_state.get('preferred_locations', []):
            missing_fields.append('Preferred locations')
        
        # Check skills
        if not session_state.get('skills', []):
            missing_fields.append('Skills')
        
        return len(missing_fields) == 0, missing_fields
    
    @staticmethod
    def validate_max_counts(session_state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that count limits are not exceeded.
        
        Args:
            session_state: Streamlit session state dictionary
            
        Returns:
            Tuple of (is_valid, list_of_violations)
        """
        violations = []
        
        # Check locations count
        locations = session_state.get('preferred_locations', [])
        if len(locations) > FormValidator.MAX_LOCATIONS:
            violations.append(f'Preferred locations ({len(locations)}) exceeds maximum of {FormValidator.MAX_LOCATIONS}')
        
        # Check positions count
        positions = session_state.get('target_positions', [])
        if len(positions) > FormValidator.MAX_POSITIONS:
            violations.append(f'Target positions ({len(positions)}) exceeds maximum of {FormValidator.MAX_POSITIONS}')
        
        # Check skills count
        skills = session_state.get('skills', [])
        if len(skills) > FormValidator.MAX_PREFERENCES:
            violations.append(f'Skills ({len(skills)}) exceeds maximum of {FormValidator.MAX_PREFERENCES}')
        
        return len(violations) == 0, violations
    
    @staticmethod
    def validate_file_upload(uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if uploaded_file is None:
            return True, ""  # No file uploaded is valid
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return False, f"File size ({uploaded_file.size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (10MB)"
        
        # Check file type
        allowed_types = ['pdf', 'docx', 'txt']
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in allowed_types:
            return False, f"File type '{file_extension}' is not supported. Allowed types: {', '.join(allowed_types)}"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return True, ""  # Empty email is valid (optional field)
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate phone number format.
        
        Args:
            phone: Phone string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone:
            return True, ""  # Empty phone is valid (optional field)
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has 10-15 digits (international format)
        if len(digits_only) < 10 or len(digits_only) > 15:
            return False, "Phone number must be 10-15 digits"
        
        return True, ""
    
    @staticmethod
    def validate_location(location: str) -> Tuple[bool, str]:
        """
        Validate location format to prevent course names and invalid data.
        
        Args:
            location: Location string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not location or not location.strip():
            return True, ""  # Empty location is valid (will be filtered out)
        
        location = location.strip()
        
        # Common course/subject keywords that should not be in locations
        invalid_keywords = [
            'course', 'class', 'subject', 'program', 'degree', 'major', 'minor',
            'bachelor', 'master', 'phd', 'doctorate', 'certificate', 'diploma',
            'computer science', 'data science', 'machine learning', 'artificial intelligence',
            'engineering', 'mathematics', 'statistics', 'business', 'economics',
            'psychology', 'biology', 'chemistry', 'physics', 'literature', 'history',
            'philosophy', 'sociology', 'political science', 'international relations',
            'accounting', 'finance', 'marketing', 'management', 'human resources',
            'nursing', 'medicine', 'law', 'education', 'architecture', 'design',
            'art', 'music', 'theater', 'dance', 'film', 'journalism', 'communication',
            # Add certification and company names
            'cisco', 'ccna', 'ccnp', 'ccie', 'microsoft', 'azure', 'aws', 'google',
            'oracle', 'java', 'python', 'javascript', 'react', 'angular', 'vue',
            'node', 'express', 'django', 'flask', 'spring', 'hibernate', 'mysql',
            'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes', 'jenkins',
            'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
            'salesforce', 'tableau', 'power bi', 'excel', 'word', 'powerpoint',
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'api', 'rest', 'graphql'
        ]
        
        location_lower = location.lower()
        
        # Check for course-related keywords
        for keyword in invalid_keywords:
            if keyword in location_lower:
                return False, f"'{location}' appears to be a course/subject name, not a location"
        
        # Check for common location patterns
        # Should contain city, state, country, or common location indicators
        location_indicators = [
            'city', 'town', 'village', 'county', 'state', 'province', 'region',
            'country', 'nation', 'island', 'peninsula', 'coast', 'valley',
            'mountain', 'hill', 'river', 'lake', 'bay', 'gulf', 'ocean',
            'remote', 'hybrid', 'onsite', 'offsite', 'virtual', 'online'
        ]
        
        # Check if it looks like a proper location
        has_location_indicator = any(indicator in location_lower for indicator in location_indicators)
        has_geographic_pattern = bool(re.search(r'[A-Z][a-z]+,\s*[A-Z]{2}', location))  # City, State pattern
        has_country_pattern = bool(re.search(r'[A-Z][a-z]+,\s*[A-Z][a-z]+', location))  # City, Country pattern
        
        if not (has_location_indicator or has_geographic_pattern or has_country_pattern):
            # Additional check: if it's a single word, it might be invalid
            if len(location.split()) == 1 and len(location) > 3:
                return False, f"'{location}' doesn't appear to be a valid location format"
        
        return True, ""
    
    @staticmethod
    def validate_position(position: str) -> Tuple[bool, str]:
        """
        Validate job position to ensure it's a proper job title.
        
        Args:
            position: Position string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not position or not position.strip():
            return True, ""  # Empty position is valid (will be filtered out)
        
        position = position.strip()
        
        # Common invalid keywords for job positions
        invalid_keywords = [
            'course', 'class', 'subject', 'program', 'degree', 'major', 'minor',
            'bachelor', 'master', 'phd', 'doctorate', 'certificate', 'diploma',
            'university', 'college', 'school', 'institute', 'academy', 'training',
            'location', 'address', 'phone', 'email', 'contact', 'resume', 'cv',
            'experience', 'skills', 'education', 'projects', 'achievements'
        ]
        
        position_lower = position.lower()
        
        # Check for invalid keywords
        for keyword in invalid_keywords:
            if keyword in position_lower:
                return False, f"'{position}' appears to be a course/subject name, not a job position"
        
        # Check for proper job title patterns
        job_title_indicators = [
            'engineer', 'developer', 'analyst', 'manager', 'director', 'coordinator',
            'specialist', 'consultant', 'advisor', 'assistant', 'associate', 'senior',
            'junior', 'lead', 'principal', 'architect', 'designer', 'researcher',
            'scientist', 'administrator', 'supervisor', 'executive', 'officer',
            'representative', 'agent', 'technician', 'operator', 'clerk', 'assistant'
        ]
        
        has_job_indicator = any(indicator in position_lower for indicator in job_title_indicators)
        
        if not has_job_indicator and len(position.split()) == 1:
            return False, f"'{position}' doesn't appear to be a valid job position"
        
        return True, ""
    
    @staticmethod
    def validate_preference(preference: str) -> Tuple[bool, str]:
        """
        Validate job preference to ensure it's a proper preference keyword.
        
        Args:
            preference: Preference string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not preference or not preference.strip():
            return True, ""  # Empty preference is valid (will be filtered out)
        
        preference = preference.strip()
        
        # Common invalid keywords for job preferences
        invalid_keywords = [
            'course', 'class', 'subject', 'program', 'degree', 'major', 'minor',
            'bachelor', 'master', 'phd', 'doctorate', 'certificate', 'diploma',
            'university', 'college', 'school', 'institute', 'academy', 'training',
            'location', 'address', 'phone', 'email', 'contact', 'resume', 'cv',
            'experience', 'education', 'projects', 'achievements', 'name', 'age'
        ]
        
        preference_lower = preference.lower()
        
        # Check for invalid keywords
        for keyword in invalid_keywords:
            if keyword in preference_lower:
                return False, f"'{preference}' appears to be a course/subject name, not a job preference"
        
        return True, ""
    
    @staticmethod
    def validate_locations_list(locations: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate a list of locations to filter out invalid entries.
        
        Args:
            locations: List of location strings to validate
            
        Returns:
            Tuple of (is_valid, list_of_invalid_entries)
        """
        invalid_entries = []
        
        for location in locations:
            is_valid, error_msg = FormValidator.validate_location(location)
            if not is_valid:
                invalid_entries.append(f"{location}: {error_msg}")
        
        return len(invalid_entries) == 0, invalid_entries
    
    @staticmethod
    def validate_positions_list(positions: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate a list of job positions to filter out invalid entries.
        
        Args:
            positions: List of position strings to validate
            
        Returns:
            Tuple of (is_valid, list_of_invalid_entries)
        """
        invalid_entries = []
        
        for position in positions:
            is_valid, error_msg = FormValidator.validate_position(position)
            if not is_valid:
                invalid_entries.append(f"{position}: {error_msg}")
        
        return len(invalid_entries) == 0, invalid_entries
    
    @staticmethod
    def validate_preferences_list(preferences: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate a list of job preferences to filter out invalid entries.
        
        Args:
            preferences: List of preference strings to validate
            
        Returns:
            Tuple of (is_valid, list_of_invalid_entries)
        """
        invalid_entries = []
        
        for preference in preferences:
            is_valid, error_msg = FormValidator.validate_preference(preference)
            if not is_valid:
                invalid_entries.append(f"{preference}: {error_msg}")
        
        return len(invalid_entries) == 0, invalid_entries
    
    @staticmethod
    def filter_valid_entries(session_state: Dict[str, Any]) -> None:
        """
        Filter out invalid entries from lists in session state.
        This is called silently to clean up the data.
        
        Args:
            session_state: Streamlit session state dictionary (modified in place)
        """
        # Filter locations
        locations = session_state.get('preferred_locations', [])
        valid_locations = []
        for location in locations:
            is_valid, _ = FormValidator.validate_location(location)
            if is_valid and location.strip():
                valid_locations.append(location.strip())
        session_state['preferred_locations'] = valid_locations
        
        # Filter positions
        positions = session_state.get('target_positions', [])
        valid_positions = []
        for position in positions:
            is_valid, _ = FormValidator.validate_position(position)
            if is_valid and position.strip():
                valid_positions.append(position.strip())
        session_state['target_positions'] = valid_positions
        
        # Filter skills
        skills = session_state.get('skills', [])
        valid_skills = []
        for skill in skills:
            is_valid, _ = FormValidator.validate_preference(skill)
            if is_valid and skill.strip():
                valid_skills.append(skill.strip())
        session_state['skills'] = valid_skills
    
    @staticmethod
    def validate_all(session_state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Perform all validations.
        
        Args:
            session_state: Streamlit session state dictionary
            
        Returns:
            Tuple of (is_valid, list_of_all_errors)
        """
        all_errors = []
        
        # Filter out invalid entries first
        FormValidator.filter_valid_entries(session_state)
        
        # Validate required fields
        is_valid_required, missing_fields = FormValidator.validate_required_fields(session_state)
        if not is_valid_required:
            all_errors.extend([f"Missing required field: {field}" for field in missing_fields])
        
        # Validate max counts
        is_valid_counts, count_violations = FormValidator.validate_max_counts(session_state)
        if not is_valid_counts:
            all_errors.extend(count_violations)
        
        # Validate email if provided
        email = session_state.get('email', '')
        is_valid_email, email_error = FormValidator.validate_email(email)
        if not is_valid_email:
            all_errors.append(f"Email validation error: {email_error}")
        
        # Validate phone if provided
        phone = session_state.get('contact', '')
        is_valid_phone, phone_error = FormValidator.validate_phone(phone)
        if not is_valid_phone:
            all_errors.append(f"Phone validation error: {phone_error}")
        
        # Validate locations list
        locations = session_state.get('preferred_locations', [])
        is_valid_locations, location_errors = FormValidator.validate_locations_list(locations)
        if not is_valid_locations:
            all_errors.extend([f"Location validation error: {error}" for error in location_errors])
        
        # Validate positions list
        positions = session_state.get('target_positions', [])
        is_valid_positions, position_errors = FormValidator.validate_positions_list(positions)
        if not is_valid_positions:
            all_errors.extend([f"Position validation error: {error}" for error in position_errors])
        
        # Validate skills list
        skills = session_state.get('skills', [])
        is_valid_skills, skill_errors = FormValidator.validate_preferences_list(skills)
        if not is_valid_skills:
            all_errors.extend([f"Skill validation error: {error}" for error in skill_errors])
        
        return len(all_errors) == 0, all_errors
    
    @staticmethod
    def enforce_max_counts(session_state: Dict[str, Any]) -> None:
        """
        Enforce maximum counts by trimming lists to limits.
        This is called silently without showing errors to the user.
        
        Args:
            session_state: Streamlit session state dictionary (modified in place)
        """
        # Trim locations
        locations = session_state.get('preferred_locations', [])
        if len(locations) > FormValidator.MAX_LOCATIONS:
            session_state['preferred_locations'] = locations[:FormValidator.MAX_LOCATIONS]
        
        # Trim positions
        positions = session_state.get('target_positions', [])
        if len(positions) > FormValidator.MAX_POSITIONS:
            session_state['target_positions'] = positions[:FormValidator.MAX_POSITIONS]
        
        # Trim skills
        skills = session_state.get('skills', [])
        if len(skills) > FormValidator.MAX_PREFERENCES:
            session_state['skills'] = skills[:FormValidator.MAX_PREFERENCES]


def validate_form_before_analysis(session_state: Dict[str, Any]) -> bool:
    """
    Validate form before running analysis. Returns True if valid, False otherwise.
    This function performs silent validation without showing errors to the user.
    
    Args:
        session_state: Streamlit session state dictionary
        
    Returns:
        bool: True if form is valid, False otherwise
    """
    # Filter out invalid entries silently
    FormValidator.filter_valid_entries(session_state)
    
    # Enforce max counts silently
    FormValidator.enforce_max_counts(session_state)
    
    # Check if all required fields are filled
    is_valid, missing_fields = FormValidator.validate_required_fields(session_state)
    
    if not is_valid:
        # Don't show error to user, just return False
        return False
    
    return True
