"""
Refactored Streamlit application using modular architecture.
This version uses separate modules for better maintainability.
"""

import streamlit as st
import time
import sys
import os
import json

# Add the Frontend directory to Python path for imports
frontend_dir = os.path.dirname(os.path.abspath(__file__))
if frontend_dir not in sys.path:
    sys.path.insert(0, frontend_dir)

# Import our custom modules
from utils.validation import validate_form_before_analysis
from utils.resume_processor import handle_file_upload
from utils.data_models import STANDARD_LOCATIONS, STANDARD_POSITIONS, STANDARD_JOB_TYPES, ALL_STANDARD_PREFERENCES
from utils.backend_integration import send_resume_data_to_backend, analyze_resume_logic, generate_job_recommendations, print_ui_data_to_terminal
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

def update_skills():
    """Update skills in session state."""
    if 'skill_select' in st.session_state:
        st.session_state.skills = st.session_state.skill_select

# Set page config first
st.set_page_config(
    page_title="AI Career Optimization Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styles
CustomCSS.apply_custom_styles()

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


def profile_analysis_tab():
    """Content for the Profile Analysis tab."""
    st.header("Profile Analysis & Data Extraction")
    st.markdown("---")

    # Info button explaining required fields
    FormComponents.info_button_with_tooltip()
    
    # Debug toggle (remove this in production)
    if st.checkbox("🐛 Debug Mode", help="Show debug information for multiselect"):
        st.session_state.debug_mode = True
    else:
        st.session_state.debug_mode = False
    
    # Resume processing status
    if st.session_state.get('gdrive_url'):
        st.info(f"📁 Resume uploaded to Google Drive: [View]({st.session_state.gdrive_url})")
    if st.session_state.get('firebase_document_id'):
        st.info(f"🔥 Firebase Document ID: `{st.session_state.firebase_document_id}`")

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
            
            # Show Resume_Parser status
            if st.session_state.raw_resume_text:
                st.success("✅ Processed with Resume_Parser (Enhanced PDF parsing)")
        
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
        
        # Debug: Show current selections
        if st.session_state.get('debug_mode', False):
            st.write(f"Debug - Selected locations: {selected_locs}")
            st.write(f"Debug - Session state locations: {st.session_state.preferred_locations}")
        
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
            print(f"TERMINAL: Attempting to add location: {location}")
            
            # Validate location before adding
            from utils.validation import FormValidator
            is_valid, error_msg = FormValidator.validate_location(location)
            
            if is_valid:
                if location not in st.session_state.preferred_locations:
                    st.session_state.preferred_locations.append(location)
                    print(f"TERMINAL: Successfully added location: {location}")
                    print(f"TERMINAL: Current locations: {st.session_state.preferred_locations}")
                    st.success(f"Added: {location}")
                else:
                    print(f"TERMINAL: Location already exists: {location}")
                    st.warning("Location already added!")
            else:
                print(f"TERMINAL: Invalid location: {location} - {error_msg}")
                st.error(f"Error: {error_msg}")
            # Removed st.rerun() to reduce lag

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
        
        # Debug: Show current selections
        if st.session_state.get('debug_mode', False):
            st.write(f"Debug - Target positions: {target_positions}")
            st.write(f"Debug - Session state positions: {st.session_state.target_positions}")

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
        
        # Debug: Show current selections
        if st.session_state.get('debug_mode', False):
            st.write(f"Debug - Selected skills: {selected_skills}")
            st.write(f"Debug - Session state skills: {st.session_state.skills}")
        
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
            print(f"TERMINAL: Attempting to add skill: {skill}")
            
            # Validate skill before adding
            from utils.validation import FormValidator
            is_valid, error_msg = FormValidator.validate_preference(skill)
            
            if is_valid:
                if skill not in st.session_state.skills:
                    st.session_state.skills.append(skill)
                    print(f"TERMINAL: Successfully added skill: {skill}")
                    print(f"TERMINAL: Current skills: {st.session_state.skills}")
                    st.success(f"Added: {skill}")
                else:
                    print(f"TERMINAL: Skill already exists: {skill}")
                    st.warning("Skill already added!")
            else:
                print(f"TERMINAL: Invalid skill: {skill} - {error_msg}")
                st.error(f"Error: {error_msg}")
            # Removed st.rerun() to reduce lag

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

    # Show loading overlay when analyzing
    if st.session_state.get('is_analyzing', False):
        LoadingOverlay.show_loading_overlay()
        
        # Perform the actual analysis
        try:
            # Send data to backend first
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
            st.rerun()


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


def job_recommendations_tab():
    """Content for the Job Recommendations tab."""
    st.header("Job Recommendations")
    st.markdown("---")
    
    if st.session_state.get('analyzed_data'):
        # Analysis Results section removed - only process final edited data
        st.success("✅ Profile analysis completed! Job recommendations generated below.")
        
        # Display webhook response if available
        if st.session_state.get('backend_data'):
            display_webhook_response()
            st.markdown("---")
        
        # Hide extracted links display
        # if st.session_state.get('extracted_links'):
        #     DisplayComponents.display_extracted_links(st.session_state.extracted_links)
        
        # Generate job recommendations
        job_recommendations = generate_job_recommendations(
            resume_text=st.session_state.raw_resume_text,
            target_positions=st.session_state.target_positions,
            preferences=st.session_state.skills,
            locations=st.session_state.preferred_locations
        )
        
        # Data was already printed to terminal after analysis completion
        
        # Convert to dict format for display
        job_recommendations_dict = [job.to_dict() for job in job_recommendations]
        
        # Display the recommendations
        DisplayComponents.display_job_recommendations(job_recommendations_dict)
        
        # Save to cloud button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("💡 Your resume has been automatically processed and saved to Google Drive and Firebase!")
    else:
        st.info("Please run the profile analysis first to see personalized job recommendations.")
        st.markdown("### How it works:")
        st.markdown("1. **Upload your resume** and fill in your preferences")
        st.markdown("2. **Click 'Analyze Profile'** to process your information")
        st.markdown("3. **View personalized job recommendations** based on your skills and experience")
        st.markdown("4. **Click on job titles** to apply directly to positions")
        st.markdown("5. **Save your complete profile to cloud** for future access")


def resume_improver_tab():
    """Content for the Resume Improver tab."""
    st.header("Resume Improvement Suggestions")
    st.markdown("---")
    
    if st.session_state.get('analyzed_data'):
        st.success("✅ Resume analysis completed!")
        
        # Show improvement suggestions
        st.markdown("### AI-Powered Improvement Suggestions")
        
        suggestions = [
            "Add more specific technical skills and certifications",
            "Include quantifiable achievements and metrics",
            "Optimize keywords for ATS (Applicant Tracking Systems)",
            "Highlight relevant project experience",
            "Include industry-specific terminology"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")
        
        # Show current resume text for editing
        st.markdown("### Edit Your Resume")
        improved_resume = st.text_area(
            "Resume Text (Editable)",
            value=st.session_state.raw_resume_text,
            height=400,
            key='improved_resume_text'
        )
        
        if st.button("💾 Save Improved Resume"):
            st.session_state.raw_resume_text = improved_resume
            st.success("Resume updated successfully!")
    else:
        st.info("Please run the profile analysis first to get improvement suggestions.")


def main():
    """Main application function."""
    # Initialize session state
    SessionStateManager.initialize_session_state()
    
    # Main title
    st.title("🚀 AI Career Optimization Tool")
    st.markdown("**Transform your career with AI-powered resume analysis and job recommendations**")
    st.markdown("---")
    
    # Debug section to check webhook response
    if st.session_state.get('backend_data'):
        st.sidebar.markdown("### 🔗 Webhook Status")
        st.sidebar.success("✅ Webhook response received!")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📋 View Response"):
                st.sidebar.json(st.session_state.backend_data)
        with col2:
            if st.button("🖥️ Print to Terminal"):
                # Use st.write to display in sidebar instead of print
                st.sidebar.markdown("**Webhook Response:**")
                st.sidebar.json(st.session_state.backend_data)
                st.sidebar.success("✅ Displayed in sidebar!")
    else:
        st.sidebar.markdown("### 🔗 Webhook Status")
        st.sidebar.info("⏳ No webhook response yet")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Profile Analysis", 
        "💼 Job Recommendations", 
        "✨ Resume Improver"
    ])

    with tab1:
        profile_analysis_tab()

    with tab2:
        job_recommendations_tab()

    with tab3:
        resume_improver_tab()


if __name__ == "__main__":
    main()