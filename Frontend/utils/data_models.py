"""
Data models module for structured data handling.
Defines data structures for resume analysis, user preferences, and API responses.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class PersonalDetails:
    """Personal details data structure."""
    full_name: str = ""
    contact: str = ""
    email: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)
    
    def is_complete(self) -> bool:
        """Check if personal details are complete."""
        return bool(self.full_name.strip())


@dataclass
class JobPreferences:
    """Job preferences data structure."""
    preferred_locations: List[str] = None
    target_positions: List[str] = None
    job_types: List[str] = None
    job_level: str = ""
    preferences: List[str] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.preferred_locations is None:
            self.preferred_locations = []
        if self.target_positions is None:
            self.target_positions = []
        if self.job_types is None:
            self.job_types = []
        if self.preferences is None:
            self.preferences = []
    
    def to_dict(self) -> Dict[str, List[str]]:
        """Convert to dictionary."""
        return asdict(self)
    
    def is_valid(self) -> bool:
        """Check if preferences are valid."""
        return len(self.preferred_locations) > 0 and len(self.preferences) > 0


@dataclass
class ResumeData:
    """Resume data structure."""
    raw_text: str = ""
    extracted_name: str = ""
    extracted_location: str = ""
    extracted_phone: str = ""
    extracted_email: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)
    
    def is_valid(self) -> bool:
        """Check if resume data is valid."""
        return bool(self.raw_text.strip())


@dataclass
class AnalysisRequest:
    """Request data structure for backend analysis."""
    resume_text: str
    personal_details: PersonalDetails
    job_preferences: JobPreferences
    timestamp: str
    user_id: str = "streamlit_user"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "resume_text": self.resume_text,
            "full_name": self.personal_details.full_name,
            "contact": self.personal_details.contact,
            "email": self.personal_details.email,
            "target_positions": self.job_preferences.target_positions,
            "job_types": self.job_preferences.job_types,
            "job_level": self.job_preferences.job_level,
            "preferences": self.job_preferences.preferences,
            "preferred_locations": self.job_preferences.preferred_locations,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class AnalysisResponse:
    """Response data structure from backend analysis."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisResponse':
        """Create from dictionary."""
        return cls(
            success=data.get('success', False),
            data=data.get('data'),
            error_message=data.get('error_message'),
            timestamp=data.get('timestamp', datetime.now().isoformat())
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class JobRecommendation:
    """Job recommendation data structure."""
    job_id: str
    title: str
    company: str
    location: str
    description: str
    date_posted: str
    salary_range: str = ""
    requirements: List[str] = None
    benefits: List[str] = None
    match_score: float = 0.0
    application_url: str = ""
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.requirements is None:
            self.requirements = []
        if self.benefits is None:
            self.benefits = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class AnalysisResults:
    """Complete analysis results data structure."""
    personal_details: PersonalDetails
    resume_data: ResumeData
    job_preferences: JobPreferences
    job_recommendations: List[JobRecommendation] = None
    analysis_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize empty lists/dicts if None."""
        if self.job_recommendations is None:
            self.job_recommendations = []
        if self.analysis_metadata is None:
            self.analysis_metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "personal_details": self.personal_details.to_dict(),
            "resume_data": self.resume_data.to_dict(),
            "job_preferences": self.job_preferences.to_dict(),
            "job_recommendations": [job.to_dict() for job in self.job_recommendations],
            "analysis_metadata": self.analysis_metadata
        }


class DataConverter:
    """Utility class for converting between different data formats."""
    
    @staticmethod
    def session_state_to_analysis_request(session_state: Dict[str, Any]) -> AnalysisRequest:
        """Convert Streamlit session state to AnalysisRequest."""
        personal_details = PersonalDetails(
            full_name=session_state.get('full_name', ''),
            contact=session_state.get('contact', ''),
            email=session_state.get('email', '')
        )
        
        job_preferences = JobPreferences(
            preferred_locations=session_state.get('preferred_locations', []),
            target_positions=session_state.get('selected_positions', []),
            job_types=session_state.get('selected_job_types', []),
            job_level=session_state.get('selected_job_level', ''),
            preferences=session_state.get('selected_preferences', [])
        )
        
        return AnalysisRequest(
            resume_text=session_state.get('raw_resume_text', ''),
            personal_details=personal_details,
            job_preferences=job_preferences,
            timestamp=datetime.now().isoformat()
        )
    
    @staticmethod
    def backend_response_to_analysis_results(
        response_data: Dict[str, Any], 
        session_state: Dict[str, Any]
    ) -> AnalysisResults:
        """Convert backend response to AnalysisResults."""
        personal_details = PersonalDetails(
            full_name=session_state.get('full_name', ''),
            contact=session_state.get('contact', ''),
            email=session_state.get('email', '')
        )
        
        resume_data = ResumeData(
            raw_text=session_state.get('raw_resume_text', ''),
            extracted_name=response_data.get('name', ''),
            extracted_location=response_data.get('preferred_location', ''),
            extracted_phone=response_data.get('phone', ''),
            extracted_email=response_data.get('email', '')
        )
        
        job_preferences = JobPreferences(
            preferred_locations=session_state.get('preferred_locations', []),
            target_positions=session_state.get('selected_positions', []),
            job_types=session_state.get('selected_job_types', []),
            job_level=session_state.get('selected_job_level', ''),
            preferences=session_state.get('selected_preferences', [])
        )
        
        # Convert job recommendations if available
        job_recommendations = []
        if 'job_recommendations' in response_data:
            for job_data in response_data['job_recommendations']:
                job_recommendations.append(JobRecommendation(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', ''),
                    location=job_data.get('location', ''),
                    salary_range=job_data.get('salary_range', ''),
                    description=job_data.get('description', ''),
                    requirements=job_data.get('requirements', []),
                    benefits=job_data.get('benefits', []),
                    match_score=job_data.get('match_score', 0.0),
                    application_url=job_data.get('application_url', '')
                ))
        
        return AnalysisResults(
            personal_details=personal_details,
            resume_data=resume_data,
            job_preferences=job_preferences,
            job_recommendations=job_recommendations,
            analysis_metadata=response_data.get('metadata', {})
        )


# Constants for the application
STANDARD_LOCATIONS = [
    "New York, NY", "San Francisco, CA", "Los Angeles, CA", "Chicago, IL",
    "Boston, MA", "Seattle, WA", "Austin, TX", "Denver, CO", "Atlanta, GA",
    "Miami, FL", "Dallas, TX", "Phoenix, AZ", "Philadelphia, PA", "Houston, TX",
    "San Diego, CA", "Portland, OR", "Nashville, TN", "Orlando, FL",
    "Las Vegas, NV", "Tampa, FL", "Remote", "Hybrid"
]

STANDARD_POSITIONS = [
    "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
    "DevOps Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Machine Learning Engineer", "Data Analyst", "Business Analyst", "Project Manager",
    "Marketing Manager", "Sales Representative", "HR Specialist", "Financial Analyst",
    "Consultant", "Research Scientist", "Technical Writer", "Quality Assurance Engineer"
]

STANDARD_JOB_TYPES = [
    "Full Time", "Part Time", "Internship", "Contract"
]

STANDARD_JOB_LEVELS = [
    "Entry Level", "Mid Level", "Senior Level"
]

ALL_STANDARD_PREFERENCES = [
    # Work Style
    "Remote Work", "Hybrid Work", "Flexible Hours", "Startup Environment",
    "Corporate Environment", "Fast-paced", "Collaborative", "Independent Work",
    
    # Technology
    "Python", "JavaScript", "React", "Node.js", "Java", "C++", "Machine Learning",
    "Artificial Intelligence", "Cloud Computing", "DevOps", "Agile", "Scrum",
    "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "SQL", "NoSQL",
    
    # Domain
    "Fintech", "Healthcare", "E-commerce", "Education", "Gaming", "Social Media",
    "Cybersecurity", "Blockchain", "IoT", "Mobile Development", "Web Development",
    "Data Science", "Analytics", "Business Intelligence", "Automation"
]
