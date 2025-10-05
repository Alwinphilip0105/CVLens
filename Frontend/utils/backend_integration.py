"""
Backend integration module for API calls.
Handles communication with backend services and data processing.
"""

import requests
import json
import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import random
import sys
import os

# Add the Frontend directory to Python path for imports
# Get the directory containing this file (utils), then go up one level (Frontend)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.dirname(current_file_dir)

# Add both the Frontend directory and the project root to sys.path
project_root = os.path.dirname(frontend_dir)  # Go up one more level to project root

for path in [frontend_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

from utils.data_models import AnalysisRequest, AnalysisResponse, DataConverter, JobRecommendation


def print_ui_data_to_terminal(session_state: Dict[str, Any], analysis_data: Dict[str, Any] = None, job_recommendations: List[JobRecommendation] = None):
    """
    Save user data to file in clean JSON format.
    
    Args:
        session_state: Streamlit session state dictionary
        analysis_data: Analysis results data
        job_recommendations: List of job recommendations (not printed)
    """
    # Extract skills from resume text (simple keyword extraction)
    resume_text = session_state.get('raw_resume_text', '')
    skills = []
    
    # Common technical skills to look for
    tech_skills = [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'React', 'Angular', 'Vue', 'Node.js',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'AWS', 'Azure', 'Docker', 'Kubernetes',
        'Git', 'Linux', 'Machine Learning', 'AI', 'Data Science', 'TensorFlow', 'PyTorch',
        'Pandas', 'NumPy', 'Scikit-learn', 'R', 'Tableau', 'Power BI', 'Excel', 'PowerPoint',
        'HTML', 'CSS', 'Bootstrap', 'jQuery', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin',
        'Spring', 'Django', 'Flask', 'Express', 'Laravel', 'Rails', 'ASP.NET', 'MongoDB',
        'Redis', 'Elasticsearch', 'Apache', 'Nginx', 'Jenkins', 'CI/CD', 'Agile', 'Scrum'
    ]
    
    # Extract skills from resume text
    resume_lower = resume_text.lower()
    for skill in tech_skills:
        if skill.lower() in resume_lower:
            skills.append(skill)
    
    # Create clean JSON data
    user_data = {
        "name": session_state.get('full_name', ''),
        "email": session_state.get('email', ''),
        "contact": session_state.get('contact', ''),
        "extracted_skills": skills,
        "selected_skills": session_state.get('skills', []),
        "target_positions": session_state.get('target_positions', []),
        "job_types": session_state.get('selected_job_types', []),
        "location_preferences": session_state.get('preferred_locations', [])
    }
    
    # Save to file
    try:
        with open('user_data_export.json', 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        
        # Also print to console (may not show in Streamlit)
        print("\n" + "="*60)
        print("USER DATA EXPORTED TO FILE: user_data_export.json")
        print("="*60)
        print(json.dumps(user_data, indent=2, ensure_ascii=False))
        print("="*60)
        print("Data export completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"Error saving data: {e}")


class BackendClient:
    """Client for communicating with backend services."""
    
    def __init__(self, base_url: str = "https://ruhack.app.n8n.cloud/webhook-test/getdata"):
        """
        Initialize backend client.
        
        Args:
            base_url: Base URL of the backend service
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = 30  # seconds
    
    def send_resume_analysis_request(self, analysis_request: AnalysisRequest) -> AnalysisResponse:
        """
        Send resume analysis request to backend.
        
        Args:
            analysis_request: AnalysisRequest object
            
        Returns:
            AnalysisResponse object
        """
        try:
            # Convert to JSON
            payload = analysis_request.to_json()
            
            # Debug: Print the data being sent (using sys.stdout to avoid Streamlit conflicts)
            import sys
            try:
                sys.stdout.write("=" * 80 + "\n")
                sys.stdout.write("🚀 WEBHOOK REQUEST TO n8n\n")
                sys.stdout.write("=" * 80 + "\n")
                sys.stdout.write(f"📍 URL: {self.base_url}\n")
                sys.stdout.write(f"📦 Payload: {payload}\n")
                sys.stdout.write("-" * 80 + "\n")
                sys.stdout.flush()
            except:
                pass  # Ignore if stdout is not available
            
            # Send request to webhook
            response = requests.post(
                self.base_url,
                headers={'Content-Type': 'application/json'},
                data=payload,
                timeout=self.timeout
            )
            
            try:
                sys.stdout.write("📥 WEBHOOK RESPONSE FROM n8n\n")
                sys.stdout.write("-" * 80 + "\n")
                sys.stdout.write(f"✅ Status Code: {response.status_code}\n")
                sys.stdout.write(f"📄 Response Headers: {dict(response.headers)}\n")
                sys.stdout.write(f"📋 Response Body: {response.text}\n")
                sys.stdout.write("=" * 80 + "\n")
                sys.stdout.flush()
            except:
                pass  # Ignore if stdout is not available
            
            if response.status_code == 200:
                response_data = response.json()
                return AnalysisResponse.from_dict(response_data)
            else:
                return AnalysisResponse(
                    success=False,
                    error_message=f"Backend error: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.Timeout:
            return AnalysisResponse(
                success=False,
                error_message="Request timeout - backend took too long to respond"
            )
        except requests.exceptions.ConnectionError:
            return AnalysisResponse(
                success=False,
                error_message="Connection error - unable to reach backend service"
            )
        except requests.exceptions.RequestException as e:
            return AnalysisResponse(
                success=False,
                error_message=f"Request failed: {str(e)}"
            )
        except json.JSONDecodeError:
            return AnalysisResponse(
                success=False,
                error_message="Invalid JSON response from backend"
            )
        except Exception as e:
            return AnalysisResponse(
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def test_connection(self) -> bool:
        """
        Test connection to webhook.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Test webhook with a simple GET request
            response = requests.get(
                self.base_url,
                timeout=5
            )
            return response.status_code in [200, 405]  # 405 Method Not Allowed is also OK for webhooks
        except:
            return False


class LocalAnalysisEngine:
    """Local analysis engine as fallback when backend is unavailable."""
    
    @staticmethod
    def analyze_resume_local(resume_text: str, positions: list, preferences: list, locations: list) -> Dict[str, Any]:
        """
        Perform local resume analysis with text extraction.
        This is a fallback when backend is not available.
        
        Args:
            resume_text: Resume text to analyze
            positions: Target positions
            preferences: Job preferences
            locations: Preferred locations
            
        Returns:
            Dictionary with analysis results
        """
        import re
        
        # Extract name (look for common patterns)
        name = "Not found"
        name_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # First Last or First Middle Last
            r'Name[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',  # Simple first last at start
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, resume_text, re.MULTILINE)
            if match:
                name = match.group(1).strip()
                break
        
        # Extract phone number
        phone = "Not found"
        phone_patterns = [
            r'(\d{1}-\d{3}-\d{3}-\d{4})',  # 1-201-952-9492
            r'(\(\d{3}\)\s*\d{3}-\d{4})',  # (201) 952-9492
            r'(\d{3}-\d{3}-\d{4})',        # 201-952-9492
            r'(\d{10})',                   # 2019529492
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, resume_text)
            if match:
                phone = match.group(1).strip()
                break
        
        # Extract email
        email = "Not found"
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        match = re.search(email_pattern, resume_text)
        if match:
            email = match.group(1).strip()
        
        # Extract location (look for city, state patterns)
        extracted_location = "Not specified"
        location_patterns = [
            r'([A-Z][a-z]+,\s*[A-Z]{2})',  # City, State (preferred format)
            r'([A-Z][a-z]+ [A-Z]{2})',  # City State (but exclude common false positives)
        ]
        
        # Common false positives to exclude
        false_positives = ['Security CC', 'Computer Science', 'Data Science', 'Machine Learning', 'Artificial Intelligence']
        
        for pattern in location_patterns:
            matches = re.findall(pattern, resume_text)
            for match in matches:
                if match.strip() not in false_positives:
                    extracted_location = match.strip()
                    break
            if extracted_location != "Not specified":
                break
        
        return {
            "name": name,
            "phone": phone,
            "email": email,
            "preferred_location": extracted_location,
            "position_matches": {pos: 75 for pos in positions}
        }


def send_resume_data_to_backend(session_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Send resume data to backend and return response.
    This function integrates with Streamlit's session state.
    
    Args:
        session_state: Streamlit session state dictionary
        
    Returns:
        Backend response data or None if failed
    """
    # Try the new simple webhook client first
    try:
        from utils.n8n_webhook_client import send_dynamic_data_to_n8n
        response_data = send_dynamic_data_to_n8n(session_state)
        
        if response_data:
            st.success("✅ Data sent to n8n webhook successfully!")
            return response_data
        else:
            st.warning("⚠️ n8n webhook failed, trying fallback method...")
    except Exception as e:
        st.warning(f"⚠️ n8n webhook error: {str(e)}, trying fallback method...")
    
    # Fallback to original method
    try:
        # Create analysis request
        analysis_request = DataConverter.session_state_to_analysis_request(session_state)
        
        # Initialize backend client
        backend_client = BackendClient()
        
        # Send request
        response = backend_client.send_resume_analysis_request(analysis_request)
        
        if response.success:
            st.success("✅ Data sent to webhook successfully!")
            return response.data
        else:
            st.warning(f"⚠️ Webhook processing failed: {response.error_message}")
            st.info("Continuing with local analysis...")
            return None
    except Exception as e:
        st.warning(f"⚠️ All webhook methods failed: {str(e)}")
        st.info("Continuing with local analysis...")
        return None


def perform_fallback_analysis(session_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform fallback analysis when backend is unavailable.
    
    Args:
        session_state: Streamlit session state dictionary
        
    Returns:
        Analysis results dictionary
    """
    return LocalAnalysisEngine.analyze_resume_local(
        resume_text=session_state.get('raw_resume_text', ''),
        positions=session_state.get('selected_positions', []),
        preferences=session_state.get('selected_preferences', []),
        locations=session_state.get('preferred_locations', [])
    )


def analyze_resume_logic(resume_text: str, positions: list, preferences: list, locations: list) -> Dict[str, Any]:
    """
    Main analysis logic that tries backend first, then falls back to local analysis.
    This function maintains compatibility with the existing codebase.
    
    Args:
        resume_text: Resume text to analyze
        positions: Target positions
        preferences: Job preferences
        locations: Preferred locations
        
    Returns:
        Analysis results dictionary
    """
    # Try backend first
    backend_client = BackendClient()
    
    if backend_client.test_connection():
        # Backend is available, use it
        analysis_request = AnalysisRequest(
            resume_text=resume_text,
            personal_details=None,  # Will be filled from session state
            job_preferences=None,   # Will be filled from session state
            timestamp=datetime.now().isoformat()
        )
        
        response = backend_client.send_resume_analysis_request(analysis_request)
        
        if response.success:
            return response.data or {}
        else:
            st.warning(f"Webhook analysis failed: {response.error_message}")
    
    # Fallback to local analysis
    return LocalAnalysisEngine.analyze_resume_local(resume_text, positions, preferences, locations)


def generate_job_recommendations(resume_text: str, target_positions: List[str], 
                                preferences: List[str], locations: List[str]) -> List[JobRecommendation]:
    """
    Generate realistic job recommendations based on resume analysis.
    
    Args:
        resume_text: Extracted resume text
        target_positions: User's target job positions
        preferences: User's job preferences
        locations: User's preferred locations
        
    Returns:
        List of JobRecommendation objects
    """
    
    # Sample job data based on common tech positions
    job_templates = [
        {
            "titles": ["Software Engineer", "Senior Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer"],
            "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Spotify", "Slack", "Zoom", "Salesforce", "Adobe", "Oracle", "IBM"],
            "descriptions": [
                "We are looking for a talented software engineer to join our growing team. You will work on cutting-edge projects and collaborate with cross-functional teams to deliver high-quality software solutions.",
                "Join our engineering team to build scalable, high-performance applications. You'll work with modern technologies and have the opportunity to make a real impact on millions of users.",
                "We're seeking a passionate developer to help us build the next generation of our platform. You'll work on challenging problems and have the freedom to innovate and experiment.",
                "Come join our team and help us build amazing products that users love. We offer a collaborative environment where you can grow your skills and advance your career.",
                "We're looking for a skilled engineer to join our team and help us scale our platform. You'll work with cutting-edge technologies and have the opportunity to learn from industry experts."
            ],
            "requirements": [
                ["Bachelor's degree in Computer Science or related field", "3+ years of software development experience", "Proficiency in Python/Java/JavaScript", "Experience with cloud platforms (AWS/GCP/Azure)", "Strong problem-solving skills"],
                ["Master's degree in Computer Science", "5+ years of experience", "Expertise in microservices architecture", "Experience with Docker and Kubernetes", "Strong leadership skills"],
                ["Bachelor's degree", "2+ years of experience", "Proficiency in React/Angular/Vue", "Experience with RESTful APIs", "Knowledge of version control systems"],
                ["Computer Science degree", "4+ years of experience", "Experience with databases (SQL/NoSQL)", "Knowledge of CI/CD pipelines", "Strong communication skills"],
                ["Relevant degree", "1+ years of experience", "Basic programming skills", "Eagerness to learn", "Team player attitude"]
            ],
            "benefits": [
                ["Competitive salary", "Health insurance", "401k matching", "Flexible work hours", "Remote work options"],
                ["Stock options", "Unlimited PTO", "Learning budget", "Gym membership", "Catered meals"],
                ["Health benefits", "Dental insurance", "Vision insurance", "Life insurance", "Disability insurance"],
                ["Professional development", "Conference attendance", "Mentorship programs", "Career growth opportunities", "Team building events"],
                ["Work-life balance", "Mental health support", "Employee assistance program", "Commuter benefits", "Pet-friendly office"]
            ],
            "salary_ranges": [
                "$80,000 - $120,000",
                "$120,000 - $180,000", 
                "$100,000 - $150,000",
                "$90,000 - $140,000",
                "$70,000 - $110,000"
            ]
        },
        {
            "titles": ["Data Scientist", "Senior Data Scientist", "Machine Learning Engineer", "Data Analyst", "Research Scientist"],
            "companies": ["Tesla", "OpenAI", "Anthropic", "Palantir", "Databricks", "Snowflake", "MongoDB", "Elastic", "Confluent", "HashiCorp", "GitLab", "Atlassian", "Twilio", "Stripe", "Square"],
            "descriptions": [
                "We're looking for a data scientist to help us extract insights from large datasets and build machine learning models that drive business decisions.",
                "Join our data science team to work on cutting-edge ML projects. You'll have the opportunity to work with state-of-the-art algorithms and massive datasets.",
                "We're seeking a talented ML engineer to help us build and deploy machine learning models at scale. You'll work with our engineering team to integrate ML solutions into our products.",
                "Come join our analytics team and help us make data-driven decisions. You'll work with stakeholders across the company to understand business needs and provide actionable insights.",
                "We're looking for a research scientist to push the boundaries of what's possible with AI and machine learning. You'll have the freedom to explore new ideas and publish your work."
            ],
            "requirements": [
                ["PhD in Data Science/ML/Statistics", "5+ years of ML experience", "Expertise in Python/R", "Experience with deep learning frameworks", "Strong mathematical background"],
                ["Master's degree in relevant field", "3+ years of experience", "Proficiency in SQL", "Experience with cloud ML platforms", "Strong analytical skills"],
                ["Bachelor's degree", "2+ years of experience", "Knowledge of statistics", "Experience with data visualization", "Strong communication skills"],
                ["Relevant degree", "1+ years of experience", "Basic programming skills", "Eagerness to learn", "Attention to detail"],
                ["PhD in Computer Science", "Research experience", "Publications in top venues", "Expertise in multiple ML domains", "Strong problem-solving skills"]
            ],
            "benefits": [
                ["Competitive salary", "Stock options", "Health insurance", "401k matching", "Flexible schedule"],
                ["Research budget", "Conference attendance", "Publication support", "Collaboration opportunities", "Cutting-edge projects"],
                ["Learning opportunities", "Mentorship", "Career development", "Team collaboration", "Innovation time"],
                ["Health benefits", "Dental insurance", "Vision insurance", "Life insurance", "Disability insurance"],
                ["Work-life balance", "Mental health support", "Employee assistance", "Commuter benefits", "Pet-friendly office"]
            ],
            "salary_ranges": [
                "$120,000 - $200,000",
                "$100,000 - $160,000",
                "$90,000 - $140,000",
                "$80,000 - $130,000",
                "$150,000 - $300,000"
            ]
        }
    ]
    
    # Generate job recommendations
    recommendations = []
    
    # Determine job category based on target positions and preferences
    job_category = 0  # Default to software engineering
    if any(keyword in ' '.join(target_positions + preferences).lower() for keyword in ['data', 'ml', 'machine learning', 'ai', 'analytics', 'statistics']):
        job_category = 1  # Data science
    
    template = job_templates[job_category]
    
    # Generate 8-12 job recommendations
    num_jobs = random.randint(8, 12)
    
    for i in range(num_jobs):
        # Generate job ID
        job_id = f"JOB-{random.randint(10000, 99999)}"
        
        # Select random title, company, description, etc.
        title = random.choice(template["titles"])
        company = random.choice(template["companies"])
        description = random.choice(template["descriptions"])
        requirements = random.choice(template["requirements"])
        benefits = random.choice(template["benefits"])
        salary_range = random.choice(template["salary_ranges"])
        
        # Select location (prefer user's preferred locations)
        if locations:
            location = random.choice(locations)
        else:
            location = random.choice(["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA", "Remote"])
        
        # Generate date posted (within last 30 days)
        days_ago = random.randint(1, 30)
        date_posted = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Generate match score (70-95%)
        match_score = round(random.uniform(0.70, 0.95), 2)
        
        # Generate application URL
        application_url = f"https://careers.{company.lower()}.com/jobs/{job_id}"
        
        # Create job recommendation
        job = JobRecommendation(
            job_id=job_id,
            title=title,
            company=company,
            location=location,
            description=description,
            date_posted=date_posted,
            salary_range=salary_range,
            requirements=requirements,
            benefits=benefits,
            match_score=match_score,
            application_url=application_url
        )
        
        recommendations.append(job)
    
    # Sort by match score (highest first)
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    
    return recommendations
