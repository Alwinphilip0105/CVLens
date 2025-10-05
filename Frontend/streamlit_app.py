"""
Refactored Streamlit application using modular architecture.
This version uses separate modules for better maintainability.
"""

import streamlit as st
import time
import sys
import os
import json
import re

# Add the Frontend directory to Python path for imports
frontend_dir = os.path.dirname(os.path.abspath(__file__))
if frontend_dir not in sys.path:
    sys.path.insert(0, frontend_dir)

# Import our custom modules
from utils.validation import validate_form_before_analysis
from utils.resume_processor import handle_file_upload
from utils.data_models import STANDARD_LOCATIONS, STANDARD_POSITIONS, STANDARD_JOB_TYPES, STANDARD_JOB_LEVELS, ALL_STANDARD_PREFERENCES
from utils.backend_integration import send_resume_data_to_backend, analyze_resume_logic, print_ui_data_to_terminal, save_combined_data_to_firestore, test_firestore_connection
from utils.ui_components import (
    LoadingOverlay, CustomCSS, FormComponents, MultiselectWithCustom, 
    DisplayComponents, SessionStateManager
)
from utils.simple_multiselect import simple_multiselect_with_custom_input, simple_multiselect

# Callback functions for multiselect updates
def update_locations():
    """Update locations in session state."""
    if 'location_select' in st.session_state:
        st.session_state.preferred_locations = st.session_state.location_select

def update_positions():
    """Update positions in session state."""
    if 'position_select' in st.session_state:
        st.session_state.target_positions = st.session_state.position_select

def update_job_types():
    """Update job types in session state."""
    if 'job_type_select' in st.session_state:
        st.session_state.selected_job_types = st.session_state.job_type_select

def update_job_level():
    """Update job level in session state."""
    if 'job_level_select' in st.session_state:
        st.session_state.selected_job_level = st.session_state.job_level_select[0] if st.session_state.job_level_select else ""

def update_skills():
    """Update skills in session state."""
    if 'skill_select' in st.session_state:
        st.session_state.skills = st.session_state.skill_select

# Set page config first
st.set_page_config(
    page_title="CVLens - AI Career Optimization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
CustomCSS.apply_custom_styles()


# Additional background and sidebar CSS
st.markdown("""
<style>
/* Main app background with more red block gradient */
.stApp {
    background: #1a0000 !important;
    background-image: 
        linear-gradient(45deg, #ff0000 25%, transparent 25%),
        linear-gradient(-45deg, #ff0000 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #cc0000 75%),
        linear-gradient(-45deg, transparent 75%, #cc0000 75%);
    background-size: 60px 60px;
    background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
    background-attachment: fixed;
}

/* Force sidebar gradient with maximum specificity */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
}

.stSidebar {
    background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
}

/* Sidebar text color */
.stSidebar .stMarkdown {
    color: #ffffff !important;
}

.stSidebar .stMarkdown h1,
.stSidebar .stMarkdown h2,
.stSidebar .stMarkdown h3 {
    color: #ffffff !important;
}

/* Sidebar buttons */
.stSidebar .stButton > button {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.stSidebar .stButton > button:hover {
    background: #007aff !important;
    color: white !important;
}

/* Job Description Panel Styling - Make expanders black */
.stExpander {
    background: #000000 !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
}

/* Target ALL possible expander header selectors */
.stExpander > div {
    background: #000000 !important;
}

.stExpander > div > div {
    background: #000000 !important;
}

.stExpander > div > div > div {
    background: #000000 !important;
}

.stExpander > div > div > div > div {
    background: #000000 !important;
    color: #ffffff !important;
}

/* Target expander header button and toggle */
.stExpander button {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: none !important;
}

.stExpander [data-testid="stExpanderToggle"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander > div[data-testid="stExpanderToggle"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the expander header area specifically */
.stExpander > div:first-child {
    background-color: #000000 !important;
}

.stExpander > div:first-child > div {
    background-color: #000000 !important;
}

.stExpander > div:first-child > div > div {
    background-color: #000000 !important;
}

/* Target all markdown content in expanders */
.stExpander .stMarkdown {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander .stMarkdown p {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target expander content area */
.stExpander > div > div > div > div > div {
    background: #2d1a1a !important;
    color: #ffffff !important;
}

/* More specific targeting for expander header */
.stExpander > div[role="button"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander > div > div[role="button"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the expander header text specifically */
.stExpander h1, .stExpander h2, .stExpander h3, .stExpander h4, .stExpander h5, .stExpander h6 {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Force black background on all expander elements */
.stExpander * {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the specific job description expander */
.stExpander[aria-expanded="true"] {
    background: #000000 !important;
}

/* Additional Streamlit-specific selectors */
.stExpander > div[data-testid="stExpanderToggle"] > div {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander > div[data-testid="stExpanderToggle"] > div > div {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the expander header text area */
.stExpander > div[data-testid="stExpanderToggle"] .stMarkdown {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Force all expander children to be black */
.stExpander > div[data-testid="stExpanderToggle"] * {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target expander header with more specificity */
div[data-testid="stExpander"] > div[data-testid="stExpanderToggle"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

div[data-testid="stExpander"] > div[data-testid="stExpanderToggle"] > div {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Override any Streamlit default styling */
.stExpander > div[data-testid="stExpanderToggle"] {
    background: #000000 !important;
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the expander header button area */
.stExpander > div[data-testid="stExpanderToggle"] button {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: none !important;
}

/* Ensure the expander header is black in all states */
.stExpander > div[data-testid="stExpanderToggle"]:hover {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander > div[data-testid="stExpanderToggle"]:active {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander > div[data-testid="stExpanderToggle"]:focus {
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stExpander[aria-expanded="true"] > div {
    background: #000000 !important;
}

/* Nuclear option - target everything with high specificity */
div[data-testid="stExpander"] {
    background: #000000 !important;
}

div[data-testid="stExpander"] > div {
    background: #000000 !important;
}

div[data-testid="stExpander"] > div > div {
    background: #000000 !important;
}

div[data-testid="stExpander"] > div > div > div {
    background: #000000 !important;
}

/* Target the expander header specifically */
div[data-testid="stExpander"] > div[data-testid="stExpanderToggle"] {
    background: #000000 !important;
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Force override any existing styles */
div[data-testid="stExpander"] > div[data-testid="stExpanderToggle"] * {
    background: #000000 !important;
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Target the expander content area */
div[data-testid="stExpander"] > div[data-testid="stExpanderContent"] {
    background: #2d1a1a !important;
    color: #ffffff !important;
}

div[data-testid="stExpander"] > div[data-testid="stExpanderContent"] * {
    background: #2d1a1a !important;
    color: #ffffff !important;
}

/* Make sure text is visible on black background */
.stExpander .stMarkdown {
    color: #ffffff !important;
}

/* Additional CSS targeting for expander headers */
.stExpander .stMarkdown p {
    color: #ffffff !important;
}

/* Center the Navigation heading */
.stSidebar .stMarkdown h2 {
    text-align: center !important;
    margin-bottom: 0.5rem !important;
    margin-top: 1rem !important;
}

/* Style the separator line */
.stSidebar hr {
    margin: 0.5rem 0 1rem 0 !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

.stExpander .stMarkdown p {
    color: #ffffff !important;
}

.stExpander .stMarkdown h1,
.stExpander .stMarkdown h2,
.stExpander .stMarkdown h3,
.stExpander .stMarkdown h4,
.stExpander .stMarkdown h5,
.stExpander .stMarkdown h6 {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# Add JavaScript to force expander styling
st.markdown("""
<script>
// Force expander headers to be black
function forceExpanderStyling() {
    // Target all expanders
    const expanders = document.querySelectorAll('[data-testid="stExpander"]');
    expanders.forEach(expander => {
        // Get the toggle element
        const toggle = expander.querySelector('[data-testid="stExpanderToggle"]');
        if (toggle) {
            toggle.style.backgroundColor = '#000000';
            toggle.style.color = '#ffffff';
            // Target all children
            const children = toggle.querySelectorAll('*');
            children.forEach(child => {
                child.style.backgroundColor = '#000000';
                child.style.color = '#ffffff';
            });
        }
        
        // Target the content area
        const content = expander.querySelector('[data-testid="stExpanderContent"]');
        if (content) {
            content.style.backgroundColor = '#2d1a1a';
            content.style.color = '#ffffff';
            const contentChildren = content.querySelectorAll('*');
            contentChildren.forEach(child => {
                child.style.backgroundColor = '#2d1a1a';
                child.style.color = '#ffffff';
            });
        }
    });
}

// Run immediately
forceExpanderStyling();

// Run when new content is added
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            setTimeout(forceExpanderStyling, 100);
        }
    });
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});
</script>
""", unsafe_allow_html=True)

# Constants
MAX_LOCATIONS = 6
MAX_POSITIONS = 5
MAX_JOB_TYPES = 4
MAX_PREFERENCES = 10


def show_resume_text_modal():
    """Show resume text editing in expander."""
    with st.expander("📝 Edit Resume Text", expanded=True):
        st.markdown("**Required:** This text will be analyzed by AI")
        
        # Resume text editor
        edited_text = st.text_area(
            "Final Resume Text Used for Analysis:",
            value=st.session_state.raw_resume_text,
            height=400,
            key='modal_resume_input',
            help="Edit your resume text here. This text will be used for AI analysis."
        )
        
        # Update session state
        st.session_state.raw_resume_text = edited_text
        
        # Action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Reset Text", key='reset_resume_btn'):
                st.session_state.raw_resume_text = ""
                st.rerun()
        
        with col2:
            if st.button("✅ Done Editing", key='done_resume_btn'):
                st.session_state.show_resume_modal = False
                st.rerun()
        
        st.info("💡 **Tip:** Manually edit the text above to ensure accuracy before running the analysis.")


def profile_analysis_page():
    """Profile Analysis page with sidebar navigation."""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Profile Analysis & Data Extraction</h3>', unsafe_allow_html=True)

    # Info button explaining required fields
    FormComponents.info_button_with_tooltip()
    
    
    # Resume processing status
    if st.session_state.get('firebase_document_id'):
        st.info(f"🔥 Resume data saved to Firestore: Document ID `{st.session_state.firebase_document_id}`")

    col_resume, col_prefs = st.columns(2)

    with col_resume:
        st.markdown("### Upload or Paste Resume *")

        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="For PDF/DOCX, please review the text area below as full conversion may require manual verification.",
            on_change=lambda: handle_file_upload(st.session_state.uploaded_file_key),
            key='uploaded_file_key'
        )

        # Resume text preview and edit button
        col1, col2 = st.columns([3, 1])
        with col1:
            # Show preview of resume text
            preview_text = st.session_state.raw_resume_text[:200] + "..." if len(st.session_state.raw_resume_text) > 200 else st.session_state.raw_resume_text
            st.text_area(
                "Resume Text Preview:",
                value=preview_text,
                height=100,
                disabled=True,
                help="Preview of your resume text. Click 'Edit Resume Text' to modify."
            )
            # Character count
            char_count = len(st.session_state.raw_resume_text)
            st.caption(f"Characters: {char_count:,}")
            
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("Edit Resume Text", key='edit_resume_btn', help="Open resume text editor"):
                st.session_state.show_resume_modal = True
        
        # Resume text modal
        if st.session_state.get('show_resume_modal', False):
            show_resume_text_modal()

        # Personal Details Section
        st.markdown("## Personal Details (Editable)")
        st.caption("💡 Personal details will be automatically extracted when you click 'Analyze Profile'")
        
        # Full Name field
        full_name_input = st.text_input("Full Name", value=st.session_state.full_name, key='full_name_input')
        st.session_state.full_name = full_name_input

        # Contact and Email
        contact_cols = st.columns(2)
        contact_input = contact_cols[0].text_input("Contact Number", value=st.session_state.contact, key='contact_input')
        email_input = contact_cols[1].text_input("Email Address", value=st.session_state.email, key='email_input')
        st.session_state.contact = contact_input
        st.session_state.email = email_input
        
        # AI-extracted location display removed as it was often inaccurate
        
        # Validation is handled automatically in the form validation functions
        
    with col_prefs:
        st.subheader("Job Preferences and Targets")

        # Preferred Locations Multi-Select
        st.markdown("**📍 Preferred Locations**")
        
        # Combine standard locations with any custom ones already selected
        current_location_options = list(STANDARD_LOCATIONS)
        for loc in st.session_state.preferred_locations:
            if loc not in current_location_options:
                current_location_options.append(loc)
        
        # Locations Multi-Select (Compact)
        selected_locs = st.multiselect(
            "Select up to 6 target locations: *",
            options=current_location_options,
            default=st.session_state.preferred_locations,
            key='location_select',
            help="**Required** - Select locations where you prefer to work",
            on_change=update_locations
        )
        
        # Update session state if changed
        if 'location_select' in st.session_state:
            st.session_state.preferred_locations = st.session_state.location_select
        
        
        # Custom location input (compact)
        col1, col2 = st.columns([4, 1])
        with col1:
            custom_location = st.text_input(
                "Add custom location:",
                placeholder="e.g., Custom City",
                key='custom_location_input'
            )
        with col2:
            add_location_clicked = st.button("Add", key='add_location_btn', help="Add custom location")
            
        # Handle location addition
        if add_location_clicked and custom_location and custom_location.strip():
            location = custom_location.strip()
            
            # Validate location before adding
            from utils.validation import FormValidator
            is_valid, error_msg = FormValidator.validate_location(location)
            
            if is_valid:
                if location not in st.session_state.preferred_locations:
                    st.session_state.preferred_locations.append(location)
                    st.success(f"Added: {location}")
                else:
                    st.warning("Location already added!")
            else:
                st.error(f"Error: {error_msg}")

        # Job Targets Multi-Select (Compact)
        st.markdown("**🎯 Target Positions**")
        target_positions = st.multiselect(
            "Select Target Positions (Max 5):",
            options=STANDARD_POSITIONS,
            default=st.session_state.target_positions,
            key='position_select',
            help="Select your target job positions",
            on_change=update_positions
        )

        # Update session state if changed
        if 'position_select' in st.session_state:
            st.session_state.target_positions = st.session_state.position_select
        
        

        # Job Types Multi-Select (Compact)
        st.markdown("**💼 Job Types**")
        selected_job_types = st.multiselect(
            "Select preferred job types:",
            options=STANDARD_JOB_TYPES,
            default=st.session_state.selected_job_types,
            key='job_type_select',
            help="Select the types of employment you're interested in",
            on_change=update_job_types
        )
        
        # Update session state if changed
        if 'job_type_select' in st.session_state:
            st.session_state.selected_job_types = st.session_state.job_type_select

        # Job Level Single Select (styled like other fields)
        st.markdown("**📊 Job Level**")
        selected_job_level = st.multiselect(
            "Select your experience level:",
            options=STANDARD_JOB_LEVELS,
            default=[st.session_state.selected_job_level] if st.session_state.selected_job_level else [],
            key='job_level_select',
            help="Select your current or target experience level",
            on_change=update_job_level,
            max_selections=1
        )
        
        # Update session state if changed (convert list to string for single selection)
        if 'job_level_select' in st.session_state:
            st.session_state.selected_job_level = st.session_state.job_level_select[0] if st.session_state.job_level_select else ""

        # Skills Multi-Select
        st.markdown("**🛠️ Skills**")
        
        # Combine standard skills with any custom ones already selected
        current_skill_options = list(ALL_STANDARD_PREFERENCES)
        for skill in st.session_state.skills:
            if skill not in current_skill_options:
                current_skill_options.append(skill)
        
        # Skills Multi-Select (Compact)
        selected_skills = st.multiselect(
            "Select your skills (Work Style, Tech, Domain): *",
            options=current_skill_options,
            default=st.session_state.skills,
            key='skill_select',
            help="**Required** - Select skills that describe your expertise",
            on_change=update_skills
        )
        
        # Update session state if changed
        if 'skill_select' in st.session_state:
            st.session_state.skills = st.session_state.skill_select
        
        
        # Custom skill input (compact)
        col1, col2 = st.columns([4, 1])
        with col1:
            custom_skill = st.text_input(
                "Add custom skill:",
                placeholder="e.g., Custom Skill",
                key='custom_skill_input'
            )
        with col2:
            add_skill_clicked = st.button("Add", key='add_skill_btn', help="Add custom skill")
            
        # Handle skill addition
        if add_skill_clicked and custom_skill and custom_skill.strip():
            skill = custom_skill.strip()
            
            # Validate skill before adding
            from utils.validation import FormValidator
            is_valid, error_msg = FormValidator.validate_preference(skill)
            
            if is_valid:
                if skill not in st.session_state.skills:
                    st.session_state.skills.append(skill)
                    st.success(f"Added: {skill}")
                else:
                    st.warning("Skill already added!")
            else:
                st.error(f"Error: {error_msg}")

    # Analyze Profile Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Analyze Profile", type="primary", use_container_width=True):
            
            # Validate form before analysis
            if validate_form_before_analysis(st.session_state):
                st.session_state.is_analyzing = True
                st.rerun()
            else:
                st.warning("Please fill in all required fields before analysis.")

    # Close the feature card
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show loading overlay when analyzing
    if st.session_state.get('is_analyzing', False):
        LoadingOverlay.show_loading_overlay()
        
        # Perform the actual analysis
        try:
            # Force update session state from multiselect components
            if 'position_select' in st.session_state:
                st.session_state.target_positions = st.session_state.position_select
            
            if 'location_select' in st.session_state:
                st.session_state.preferred_locations = st.session_state.location_select
            
            if 'skill_select' in st.session_state:
                st.session_state.skills = st.session_state.skill_select
            
            if 'job_type_select' in st.session_state:
                st.session_state.selected_job_types = st.session_state.job_type_select
            
            if 'job_level_select' in st.session_state:
                st.session_state.selected_job_level = st.session_state.job_level_select[0] if st.session_state.job_level_select else ""
            
            # Test Firestore connection first
            if not test_firestore_connection():
                st.error("❌ Cannot connect to Firestore. Please check Firebase configuration.")
                st.session_state.is_analyzing = False
                st.rerun()
                return
            
            # Save combined data to Firestore first
            firestore_doc_id = save_combined_data_to_firestore(st.session_state)
            
            if firestore_doc_id:
                st.success("✅ Combined data saved to Firestore successfully!")
                st.info(f"🔥 Firestore Document ID: `{firestore_doc_id}`")
            else:
                st.warning("⚠️ Failed to save data to Firestore")
            
            # Send data to backend/n8n
            backend_response = send_resume_data_to_backend(st.session_state)
            
            if backend_response:
                st.session_state.backend_data = backend_response
                
                # Display webhook response data
                st.success("✅ Webhook response received!")
                with st.expander("📋 View Webhook Response Data"):
                    st.json(backend_response)
            
            # Continue with local analysis
            data = analyze_resume_logic(
                st.session_state.raw_resume_text, 
                st.session_state.target_positions, 
                st.session_state.skills,
                st.session_state.preferred_locations
            )
            
            if data:
                st.session_state.analyzed_data = data
                
                # Update session state with analysis results
                SessionStateManager.update_session_state_from_analysis(data)
                
                # Print user data to terminal immediately after analysis
                print_ui_data_to_terminal(
                    session_state=st.session_state,
                    analysis_data=data,
                    job_recommendations=None
                )

                # Rerun to update the input widgets with new state values
                st.experimental_rerun()
            else:
                st.session_state.analyzed_data = None
    
        except Exception as e:
            st.error(f"Analysis failed: {e}")
        finally:
            # Clear loading state
            st.session_state.is_analyzing = False
            # Switch to job recommendations page after analysis completion
            st.session_state.current_page = "jobs"
            st.rerun()


def extract_job_recommendations_from_webhook(webhook_data):
    """Extract job recommendations from elements 1 onwards of webhook response."""
    try:
        if isinstance(webhook_data, list) and len(webhook_data) > 1:
            # Return elements from index 1 onwards (skip 0th element which is resume tips)
            return webhook_data[1:]
        elif isinstance(webhook_data, dict):
            # Check if data is in 'data' key
            if 'data' in webhook_data and isinstance(webhook_data['data'], list) and len(webhook_data['data']) > 1:
                return webhook_data['data'][1:]
            # Check if job recommendations are in a specific key
            elif 'job_recommendations' in webhook_data:
                return webhook_data['job_recommendations']
            # Check if job recommendations are in 'jobs' key
            elif 'jobs' in webhook_data:
                return webhook_data['jobs']
        
        return []
    except Exception as e:
        print(f"Error extracting job recommendations: {e}")
        return []


def display_webhook_job_recommendations(job_data_list):
    """Display job recommendations from webhook data in a nice format."""
    if not job_data_list:
        st.warning("No job recommendations found in webhook response.")
        return
    
    st.markdown("### 🎯 AI-Generated Job Recommendations")
    st.info("💡 These recommendations are generated based on your resume analysis and preferences.")
    st.markdown("---")
    
    for i, job_data in enumerate(job_data_list, 1):
        # Create a job card
        with st.container():
            st.markdown(f"#### 💼 **{i}. {job_data.get('title', 'Job Title Not Available')}**")
            
            # Company and location
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**🏢 Company:** {job_data.get('company', 'Company Not Specified')}")
            with col2:
                st.markdown(f"**📍 Location:** {job_data.get('location', 'Location Not Specified')}")
            
            # Salary and match score
            col1, col2 = st.columns([2, 1])
            with col1:
                salary = job_data.get('salary_range', job_data.get('salary', 'Salary Not Specified'))
                st.markdown(f"**💰 Salary:** {salary}")
            with col2:
                # Calculate match score from job score (0-1) to percentage (0-100)
                job_score = job_data.get('job_score', job_data.get('score', None))
                match_score = job_data.get('match_score', job_data.get('match', None))
                
                if job_score is not None and isinstance(job_score, (int, float)):
                    # Convert 0-1 score to 0-100 percentage and round to 2 decimal places
                    match_percentage = round(float(job_score) * 100, 2)
                    st.markdown(f"**🎯 Match:** {match_percentage}%")
                elif match_score is not None and isinstance(match_score, (int, float)):
                    # If match_score is already a percentage, use it directly
                    if 0 <= match_score <= 1:
                        # If it's between 0-1, convert to percentage and round to 2 decimal places
                        match_percentage = round(float(match_score) * 100, 2)
                        st.markdown(f"**🎯 Match:** {match_percentage}%")
                    else:
                        # If it's already a percentage, round to 2 decimal places
                        match_percentage = round(float(match_score), 2)
                        st.markdown(f"**🎯 Match:** {match_percentage}%")
                else:
                    st.markdown("**🎯 Match:** N/A")
            
            # Job description if available
            if 'description' in job_data and job_data['description']:
                with st.expander("📝 **Job Description**", expanded=False):
                    st.markdown(job_data['description'])
            
            # Requirements if available
            if 'requirements' in job_data and job_data['requirements']:
                with st.expander("📋 **Requirements**", expanded=False):
                    if isinstance(job_data['requirements'], list):
                        for req in job_data['requirements']:
                            st.markdown(f"• {req}")
                    else:
                        st.markdown(job_data['requirements'])
            
            # Skills if available
            if 'skills' in job_data and job_data['skills']:
                with st.expander("🛠️ **Required Skills**", expanded=False):
                    if isinstance(job_data['skills'], list):
                        for skill in job_data['skills']:
                            st.markdown(f"• {skill}")
                    else:
                        st.markdown(job_data['skills'])
            
            # Apply button
            if 'url' in job_data and job_data['url']:
                st.markdown(f"[🔗 Apply Now]({job_data['url']})")
            elif 'link' in job_data and job_data['link']:
                st.markdown(f"[🔗 Apply Now]({job_data['link']})")
            
            st.markdown("---")


def display_webhook_response():
    """Display webhook response data if available."""
    if st.session_state.get('backend_data'):
        st.markdown("### 🔗 n8n Webhook Response")
        st.markdown("---")
        
        # Display the raw response
        st.json(st.session_state.backend_data)
        
        # Try to extract specific data if it exists
        response_data = st.session_state.backend_data
        
        if isinstance(response_data, dict):
            # Display key information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Response Summary:**")
                st.write(f"✅ Success: {response_data.get('success', 'Unknown')}")
                st.write(f"📅 Timestamp: {response_data.get('timestamp', 'Unknown')}")
                
            with col2:
                if 'data' in response_data:
                    data = response_data['data']
                    st.markdown("**Extracted Data:**")
                    if 'name' in data:
                        st.write(f"👤 Name: {data['name']}")
                    if 'email' in data:
                        st.write(f"📧 Email: {data['email']}")
                    if 'phone' in data:
                        st.write(f"📞 Phone: {data['phone']}")
                    if 'preferred_location' in data:
                        st.write(f"📍 Location: {data['preferred_location']}")
            
            # Display job recommendations if available
            if 'data' in response_data and 'job_recommendations' in response_data['data']:
                st.markdown("**Job Recommendations from Webhook:**")
                job_recs = response_data['data']['job_recommendations']
                for i, job in enumerate(job_recs, 1):
                    st.write(f"{i}. **{job.get('title', 'N/A')}** at {job.get('company', 'N/A')}")
                    st.write(f"   Location: {job.get('location', 'N/A')}")
                    st.write(f"   Salary: {job.get('salary_range', 'N/A')}")
                    st.write(f"   Match: {job.get('match_score', 'N/A')}")
                    st.write("---")


def job_recommendations_page():
    """Job Recommendations page with sidebar navigation."""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h3>💼 Job Recommendations</h3>', unsafe_allow_html=True)
    
    if st.session_state.get('analyzed_data'):
        # Analysis Results section removed - only process final edited data
        st.success("✅ Profile analysis completed! Job recommendations generated below.")
        
        # Check if we have webhook response data
        if st.session_state.get('backend_data'):
            # Extract job recommendations from elements 1 onwards (skip 0th which is resume tips)
            job_recommendations_data = extract_job_recommendations_from_webhook(st.session_state.backend_data)
            
            if job_recommendations_data:
                # Display job recommendations from webhook
                display_webhook_job_recommendations(job_recommendations_data)
            else:
                # Check if we have any data at all (even if just resume tips)
                webhook_data = st.session_state.backend_data
                if isinstance(webhook_data, list) and len(webhook_data) == 1:
                    display_no_job_recommendations_message("resume_tips_only")
                else:
                    display_no_job_recommendations_message("no_data")
        else:
            display_no_job_recommendations_message("no_webhook")
        
        # Save to cloud button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("💡 Your resume has been automatically processed and saved to Firestore!")
    else:
        st.info("Please run the profile analysis first to see personalized job recommendations.")
        st.markdown("### How it works:")
        st.markdown("1. **Upload your resume** and fill in your preferences")
        st.markdown("2. **Click 'Analyze Profile'** to process your information")
        st.markdown("3. **View personalized job recommendations** based on your skills and experience")
        st.markdown("4. **Click on job titles** to apply directly to positions")
        st.markdown("5. **Save your complete profile to cloud** for future access")
    
    # Close the feature card
    st.markdown('</div>', unsafe_allow_html=True)


def display_no_job_recommendations_message(scenario):
    """Display appropriate message when no job recommendations are available."""
    st.markdown("### 🎯 Job Recommendations")
    
    if scenario == "resume_tips_only":
        st.info("ℹ️ **No job recommendations found in the analysis response.**")
        st.markdown("The AI analysis focused on resume improvement suggestions but didn't generate specific job recommendations.")
        
        st.markdown("**This could happen if:**")
        st.markdown("• Your profile needs more specific targeting for job matching")
        st.markdown("• The job recommendation service needs additional criteria")
        st.markdown("• The analysis prioritized resume improvement over job matching")
        
    elif scenario == "no_data":
        st.warning("⚠️ **No job recommendations found in the webhook response.**")
        st.markdown("The analysis completed but didn't return any job recommendation data.")
        
    elif scenario == "no_webhook":
        st.warning("⚠️ **No analysis data available.**")
        st.markdown("Please run the profile analysis first to get personalized job recommendations.")
    
    st.markdown("---")
    
    # Suggestions for improvement
    st.markdown("### 💡 **How to get job recommendations:**")
    st.markdown("1. **Complete your profile** with detailed skills and preferences")
    st.markdown("2. **Specify your target positions** and job levels")
    st.markdown("3. **Add your preferred locations** for better matching")
    st.markdown("4. **Re-run the analysis** to get updated recommendations")
    
    # Try again button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 **Try Analysis Again**", use_container_width=True):
            st.session_state.current_page = "profile"
            st.rerun()


def extract_resume_tips_from_webhook(webhook_data):
    """Extract resume tips from the 0th object of webhook response."""
    try:
        if isinstance(webhook_data, list) and len(webhook_data) > 0:
            # Handle array format - get 0th element
            first_element = webhook_data[0]
            if isinstance(first_element, dict) and 'text' in first_element:
                return first_element['text']
            return first_element
        elif isinstance(webhook_data, dict):
            # Check if data is in 'data' key
            if 'data' in webhook_data and isinstance(webhook_data['data'], list) and len(webhook_data['data']) > 0:
                first_element = webhook_data['data'][0]
                if isinstance(first_element, dict) and 'text' in first_element:
                    return first_element['text']
                return first_element
            # Check if tips are in a specific key
            elif 'resume_tips' in webhook_data:
                return webhook_data['resume_tips']
            # Check if tips are in 'tips' key
            elif 'tips' in webhook_data:
                return webhook_data['tips']
        
        return None
    except Exception as e:
        print(f"Error extracting resume tips: {e}")
        return None


def parse_tips_text(tips_text):
    """Parse tips text to extract headings and bullet points."""
    if not tips_text:
        return []
    
    # Split by lines and process
    lines = tips_text.strip().split('\n')
    parsed_tips = []
    current_section = None
    intro_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a main heading (numbered sections like "1. **Formatting & Layout**")
        if re.match(r'^\d+\.\s*\*\*.*\*\*', line):
            # Save previous section if exists
            if current_section:
                parsed_tips.append(current_section)
            
            # Start new section - extract heading without ** markers
            heading = re.sub(r'^\d+\.\s*\*\*(.*)\*\*.*', r'\1', line).strip()
            current_section = {
                'heading': heading,
                'content': [],
                'bullets': []
            }
        
        # Check if it's a main heading without ** markers (like "1. Formatting & Layout:")
        elif re.match(r'^\d+\.\s+[A-Za-z].*:', line):
            # Save previous section if exists
            if current_section:
                parsed_tips.append(current_section)
            
            # Start new section - extract heading
            heading = re.sub(r'^\d+\.\s+(.*):.*', r'\1', line).strip()
            current_section = {
                'heading': heading,
                'content': [],
                'bullets': []
            }
        
        # Check if it's a main heading with emoji (like "📋 1. Refine Summary:")
        elif re.match(r'^[📝✨💼🛠️🎓🏆⭐🚀📋]+\s+\d+\.\s+[A-Za-z].*:', line):
            # Save previous section if exists
            if current_section:
                parsed_tips.append(current_section)
            
            # Start new section - extract heading (remove emoji and number)
            heading = re.sub(r'^[📝✨💼🛠️🎓🏆⭐🚀📋]+\s+\d+\.\s+(.*):.*', r'\1', line).strip()
            current_section = {
                'heading': heading,
                'content': [],
                'bullets': []
            }
        
        # Check if it's a subheading (like "**Readability:**")
        elif line.startswith('**') and line.endswith('**') and ':' in line:
            if current_section:
                # Remove ** markers completely
                clean_text = line.replace('**', '').strip()
                current_section['content'].append(clean_text)
        
        # Check if it's a bullet point (starts with * or -)
        elif line.startswith(('*', '-')) and not line.startswith('**'):
            bullet_text = line.lstrip('*- ').strip()
            if current_section:
                current_section['bullets'].append(bullet_text)
            else:
                # If no current section, add to intro text
                intro_text.append(line)
        
        # Check if it's a sub-bullet point (indented)
        elif line.startswith(('  *', '  -', '    *', '    -')):
            bullet_text = line.lstrip(' *-').strip()
            if current_section:
                current_section['bullets'].append(f"  • {bullet_text}")
            else:
                # If no current section, add to intro text
                intro_text.append(line)
        
        # Regular content
        else:
            if current_section:
                current_section['content'].append(line)
            else:
                # If no current section, add to intro text
                intro_text.append(line)
    
    # Add the last section
    if current_section:
        parsed_tips.append(current_section)
    
    # Add intro text as a special section
    if intro_text:
        parsed_tips.insert(0, {
            'heading': 'Introduction',
            'content': intro_text,
            'bullets': [],
            'is_intro': True
        })
    
    return parsed_tips


def display_formatted_resume_tips(tips_data):
    """Display formatted resume tips with proper UI components."""
    if isinstance(tips_data, str):
        # Parse the text format
        parsed_tips = parse_tips_text(tips_data)
    elif isinstance(tips_data, dict):
        # Handle structured data
        parsed_tips = [tips_data]
    elif isinstance(tips_data, list):
        # Handle list of tips
        parsed_tips = tips_data
    else:
        st.error("Unable to parse tips data format.")
        return
    
    if not parsed_tips:
        st.warning("No tips data found to display.")
        return
    
    # Display each tip section
    for i, tip_section in enumerate(parsed_tips, 1):
        if isinstance(tip_section, dict):
            heading = tip_section.get('heading', f'Tip {i}')
            content = tip_section.get('content', [])
            bullets = tip_section.get('bullets', [])
            is_intro = tip_section.get('is_intro', False)
            
            # Handle introduction text differently (no expandable section)
            if is_intro:
                st.markdown("### 📋 Resume Analysis Overview")
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                st.markdown("---")
            else:
                # Create expandable section with emoji based on heading
                emoji = get_section_emoji(heading)
                with st.expander(f"{emoji} **{i-1}. {heading}**", expanded=(i == 2)):  # First numbered section expanded
                    # Display content paragraphs
                    if content:
                        for paragraph in content:
                            if paragraph.strip():
                                # Process bold text formatting
                                processed_paragraph = process_bold_text(paragraph)
                                st.markdown(processed_paragraph)
                    
                    # Display bullet points with proper formatting
                    if bullets:
                        for bullet in bullets:
                            if bullet.strip():
                                # Process bold text formatting
                                processed_bullet = process_bold_text(bullet)
                                # Handle indented bullets
                                if bullet.startswith('  •'):
                                    st.markdown(f"  {processed_bullet}")
                                else:
                                    st.markdown(f"• {processed_bullet}")
        else:
            # Handle simple string tips
            st.markdown(f"**{i}.** {tip_section}")


def process_bold_text(text):
    """Process text to remove all ** markers."""
    # Remove all ** markers from the text
    clean_text = text.replace('**', '')
    return clean_text


def get_section_emoji(heading):
    """Get appropriate emoji based on section heading."""
    heading_lower = heading.lower()
    
    if 'formatting' in heading_lower or 'layout' in heading_lower:
        return "📝"
    elif 'clarity' in heading_lower or 'conciseness' in heading_lower:
        return "✨"
    elif 'experience' in heading_lower or 'professional' in heading_lower:
        return "💼"
    elif 'skills' in heading_lower or 'technical' in heading_lower:
        return "🛠️"
    elif 'education' in heading_lower or 'certification' in heading_lower:
        return "🎓"
    elif 'achievement' in heading_lower or 'project' in heading_lower:
        return "🏆"
    elif 'impression' in heading_lower or 'strength' in heading_lower:
        return "⭐"
    elif 'improvement' in heading_lower:
        return "🚀"
    else:
        return "📋"


def display_default_resume_tips():
    """Display default resume tips when no personalized data is available."""
    st.markdown("### 🎯 Essential Resume Tips")
    
    # Tip 1: Formatting
    with st.expander("📝 **1. Professional Formatting**", expanded=True):
        st.markdown("""
        **Key Points:**
        - Use a clean, professional font (Arial, Calibri, or Times New Roman)
        - Keep font size between 10-12 points
        - Use consistent formatting throughout
        - Include proper spacing and margins
        - Save as PDF to preserve formatting
        """)
    
    # Tip 2: Content Structure
    with st.expander("🏗️ **2. Content Structure**", expanded=False):
        st.markdown("""
        **Recommended Sections:**
        - **Contact Information**: Name, phone, email, LinkedIn
        - **Professional Summary**: 2-3 lines highlighting your value
        - **Work Experience**: Most recent first, use action verbs
        - **Education**: Degree, institution, graduation year
        - **Skills**: Technical and soft skills relevant to the job
        - **Certifications**: Professional certifications and licenses
        """)
    
    # Tip 3: Keywords
    with st.expander("🔍 **3. ATS Optimization**", expanded=False):
        st.markdown("""
        **ATS (Applicant Tracking System) Tips:**
        - Include relevant keywords from the job description
        - Use standard section headings (Experience, Education, Skills)
        - Avoid graphics, tables, or complex formatting
        - Use common file formats (PDF or Word)
        - Include variations of important terms
        """)
    
    # Tip 4: Quantify Achievements
    with st.expander("📊 **4. Quantify Your Achievements**", expanded=False):
        st.markdown("""
        **Use Numbers and Metrics:**
        - "Increased sales by 25% in Q3"
        - "Managed a team of 12 employees"
        - "Reduced costs by $50,000 annually"
        - "Improved customer satisfaction by 15%"
        - "Led 5 successful projects worth $2M total"
        """)
    
    # Tip 5: Tailoring
    with st.expander("🎯 **5. Tailor for Each Job**", expanded=False):
        st.markdown("""
        **Customization Strategy:**
        - Study the job description carefully
        - Match your skills to their requirements
        - Use their language and terminology
        - Highlight relevant experience first
        - Remove irrelevant information
        """)
    
    # Interactive Resume Builder
    st.markdown("---")
    st.markdown("### 🛠️ Interactive Resume Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Resume Analysis:**")
        if st.session_state.get('analyzed_data'):
            st.success("✅ Resume analyzed successfully!")
            
            # Show improvement suggestions
            suggestions = [
                "Add more specific technical skills",
                "Include quantifiable achievements",
                "Optimize keywords for ATS",
                "Highlight relevant project experience",
                "Include industry-specific terminology"
            ]
            
            for i, suggestion in enumerate(suggestions, 1):
                st.write(f"{i}. {suggestion}")
        else:
            st.info("Upload and analyze your resume to get personalized suggestions.")
    
    with col2:
        st.markdown("**Resume Score:**")
        if st.session_state.get('analyzed_data'):
            # Calculate a mock score based on content
            score = 85  # This would be calculated based on actual analysis
            st.metric("Overall Score", f"{score}/100")
            
            # Progress bar
            st.progress(score / 100)
            
            if score >= 80:
                st.success("Great job! Your resume is well-optimized.")
            elif score >= 60:
                st.warning("Good foundation, but room for improvement.")
            else:
                st.error("Consider significant improvements to your resume.")
        else:
            st.info("Analyze your resume to see your score.")
    
    # Resume Editing Section
    st.markdown("---")
    st.markdown("### ✏️ Edit Your Resume")
    
    if st.session_state.get('raw_resume_text'):
        st.markdown("**Current Resume Text:**")
        improved_resume = st.text_area(
            "Resume Text (Editable)",
            value=st.session_state.raw_resume_text,
            height=400,
            key='improved_resume_text',
            help="Edit your resume text here. Use the tips above to improve it."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Improved Resume", use_container_width=True):
                st.session_state.raw_resume_text = improved_resume
                st.success("Resume updated successfully!")
        
        with col2:
            if st.button("🔄 Reset to Original", use_container_width=True):
                st.rerun()
    else:
        st.info("Please upload and analyze your resume first to access the editing features.")
    
    # Close the feature card
    st.markdown('</div>', unsafe_allow_html=True)


def resume_tips_page():
    """Resume Tips page with sidebar navigation."""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h3>✨ Resume Tips & Improvement Guide</h3>', unsafe_allow_html=True)
    
    # Check if we have webhook response data
    if st.session_state.get('backend_data'):
        # Extract resume tips from 0th object of webhook response
        tips_data = extract_resume_tips_from_webhook(st.session_state.backend_data)
        
        if tips_data:
            st.markdown("### 🎯 Personalized Resume Tips")
            st.info("💡 These tips are generated based on your specific resume and profile analysis.")
            st.markdown("---")
            
            # Display the formatted tips
            display_formatted_resume_tips(tips_data)
        else:
            st.warning("⚠️ No personalized tips available. Please run profile analysis first.")
            display_default_resume_tips()
    else:
        st.info("📝 Upload and analyze your resume to get personalized improvement suggestions.")
        display_default_resume_tips()
    
    # Close the feature card
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application function."""
    # Initialize session state
    SessionStateManager.initialize_session_state()
    
    # Main container with modern design
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header section
    st.markdown('''
    <div class="app-header">
        <h1 class="app-title">🚀 CVLens</h1>
        <p class="app-subtitle">Transform your career with AI-powered resume analysis and job recommendations</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("📊 Profile Analysis", use_container_width=True, key="nav_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        
        if st.button("💼 Job Recommendations", use_container_width=True, key="nav_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()
        
        if st.button("✨ Resume Tips", use_container_width=True, key="nav_tips"):
            st.session_state.current_page = "tips"
            st.rerun()
        
        st.markdown("---")
        
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "profile"
    
    # Main content area based on selected page
    if st.session_state.current_page == "profile":
        profile_analysis_page()
    elif st.session_state.current_page == "jobs":
        job_recommendations_page()
    elif st.session_state.current_page == "tips":
        resume_tips_page()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()