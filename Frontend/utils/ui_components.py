"""
UI components module for reusable Streamlit components.
Contains reusable UI elements and styling.
"""

import streamlit as st
from typing import List, Optional, Callable


class LoadingOverlay:
    """Handles full-screen loading overlay display."""
    
    @staticmethod
    def show_loading_overlay():
        """Display full-screen animated loading overlay."""
        st.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-family: Arial, sans-serif;
        ">
            <div style="text-align: center;">
                <div style="
                    width: 80px;
                    height: 80px;
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #3498db;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                "></div>
                <h2 style="margin: 0; color: #3498db;">🚀 Analyzing Your Profile</h2>
                <p style="margin: 10px 0; font-size: 16px;">Please wait while we process your resume and fetch job recommendations...</p>
                <div style="margin-top: 20px;">
                    <div style="
                        width: 300px;
                        height: 4px;
                        background-color: #333;
                        border-radius: 2px;
                        overflow: hidden;
                        margin: 0 auto;
                    ">
                        <div style="
                            width: 100%;
                            height: 100%;
                            background: linear-gradient(90deg, #3498db, #2ecc71);
                            animation: progress 3s ease-in-out infinite;
                        "></div>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes progress {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(0%); }
            100% { transform: translateX(100%); }
        }
        </style>
        """, unsafe_allow_html=True)


class CustomCSS:
    """Handles custom CSS styling for the application."""
    
    @staticmethod
    def apply_custom_styles():
        """Apply custom CSS styles to the application."""
        st.markdown("""
        <style>
            .compact-input {
                margin-bottom: 0.5rem;
            }
            .chip-button {
                background-color: #f0f2f6;
                border: 1px solid #d1d5db;
                border-radius: 20px;
                padding: 0.25rem 0.75rem;
                font-size: 0.875rem;
                margin: 0.125rem;
                display: inline-block;
            }
            .chip-button:hover {
                background-color: #e5e7eb;
            }
            /* Custom styling for job function buttons */
            .stButton > button {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 20px;
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
                transition: all 0.2s;
                width: 100%;
                text-align: center;
            }
            .stButton > button:hover {
                background-color: #c3e6cb;
                transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            /* Selected state for primary buttons */
            .stButton > button[kind="primary"] {
                background-color: #28a745;
                color: white;
                border-color: #1e7e34;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #218838;
            }
            /* Style multiselect chips to look like the image */
            .stMultiSelect > div > div {
                background-color: #dc3545;
                color: white;
                border-radius: 20px;
                padding: 4px 8px;
                margin: 2px;
                font-size: 0.9rem;
            }
            .stMultiSelect > div > div > span {
                color: white;
            }
            .stMultiSelect > div > div > button {
                color: white;
                background: none;
                border: none;
                margin-left: 4px;
            }
            /* Make asterisks red using CSS */
            .red-asterisk {
                color: red;
            }
            /* Target Streamlit label elements */
            .stTextInput label,
            .stTextArea label,
            .stMultiSelect label,
            .stMarkdownContainer h3,
            .stMarkdownContainer p {
                color: inherit;
            }
            /* Make asterisks red in specific contexts */
            .stMarkdownContainer h3:after,
            .stMarkdownContainer p:after {
                content: "";
            }
            
            /* Sidebar Styling - Multiple selectors for compatibility */
            .css-1d391kg,
            .stSidebar,
            [data-testid="stSidebar"],
            .css-1cypcdb,
            .css-1v0mbdj {
                background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                position: relative;
                overflow: hidden;
            }
            
            /* Add subtle overlay for depth */
            .css-1d391kg::before,
            .stSidebar::before,
            [data-testid="stSidebar"]::before,
            .css-1cypcdb::before,
            .css-1v0mbdj::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
                pointer-events: none;
                z-index: 1;
            }
            
            /* Ensure sidebar content is above overlay */
            .stSidebar > * {
                position: relative;
                z-index: 2;
            }
            
            /* Additional sidebar targeting for older Streamlit versions */
            section[data-testid="stSidebar"] {
                background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
            }
            
            /* Force sidebar background with higher specificity */
            .stApp > div:first-child {
                background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
            }
            
            /* Target sidebar container directly */
            div[data-testid="stSidebar"] {
                background: linear-gradient(135deg, #0d0505 0%, #1a0a0a 25%, #2d0d0d 50%, #3d1515 75%, #4d1a1a 100%) !important;
            }
            
            .stSidebar .stButton > button {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 0.75rem 1rem;
                font-weight: 500;
                transition: all 0.2s ease;
                margin-bottom: 0.5rem;
            }
            
            .stSidebar .stButton > button:hover {
                background: #007aff;
                color: white;
                border-color: #007aff;
                transform: translateX(4px);
            }
            
            .stSidebar .stButton > button:active {
                background: #0056b3;
            }
            
            /* Sidebar navigation active state */
            .stSidebar .stButton > button[aria-pressed="true"] {
                background: #007aff;
                color: white;
                border-color: #007aff;
            }
            
            /* Sidebar content styling */
            .stSidebar .stMarkdown {
                color: #ffffff;
            }
            
            .stSidebar .stMarkdown h1,
            .stSidebar .stMarkdown h2,
            .stSidebar .stMarkdown h3,
            .stSidebar .stMarkdown h4,
            .stSidebar .stMarkdown h5,
            .stSidebar .stMarkdown h6 {
                color: #ffffff;
            }
            
            .stSidebar .stSuccess {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 0.75rem;
            }
            
            .stSidebar .stInfo {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
                border-radius: 8px;
                padding: 0.75rem;
            }
            
            /* Main content area adjustments for sidebar */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
        </style>
        <script>
            // Function to make asterisks red
            function makeAsterisksRed() {
                // Find all text nodes and make asterisks red
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                while (node = walker.nextNode()) {
                    if (node.textContent.includes('*')) {
                        const parent = node.parentNode;
                        if (parent && parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE') {
                            const html = node.textContent.replace(/\*/g, '<span style="color: red;">*</span>');
                            const wrapper = document.createElement('span');
                            wrapper.innerHTML = html;
                            parent.replaceChild(wrapper, node);
                        }
                    }
                }
            }
            
            // Run when page loads
            document.addEventListener('DOMContentLoaded', makeAsterisksRed);
            
            // Run when Streamlit updates content
            if (window.parent !== window) {
                const observer = new MutationObserver(makeAsterisksRed);
                observer.observe(document.body, { childList: true, subtree: true });
            }
        </script>
        """, unsafe_allow_html=True)


class FormComponents:
    """Reusable form components."""
    
    @staticmethod
    def required_field_label(text: str) -> str:
        """Create a label with red asterisk for required fields."""
        return f"{text} *"
    
    @staticmethod
    def required_field_label_html(text: str) -> str:
        """Create a label with red asterisk for required fields (HTML version)."""
        return f"{text} <span style='color: red;'>*</span>"
    
    @staticmethod
    def info_button_with_tooltip():
        """Display info button with hoverable transparent tab effect explaining required fields."""
        st.markdown("""
        <div style="position: relative; display: inline-block; margin-bottom: 10px;">
            <button id="infoButton" style="
                background: rgba(31, 119, 180, 0.8);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                width: 32px;
                height: 32px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
            " onmouseover="showTooltip()" onmouseout="hideTooltip()">
                <span style="position: relative; z-index: 2;">i</span>
                <div id="hoverOverlay" style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    border-radius: 50%;
                "></div>
            </button>
            <div id="infoTooltip" style="
                position: absolute;
                background: rgba(0, 0, 0, 0.85);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                font-size: 13px;
                white-space: nowrap;
                z-index: 1000;
                top: 40px;
                left: -60px;
                display: none;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(15px);
                min-width: 220px;
                white-space: normal;
                line-height: 1.5;
                transform: translateY(-10px);
                opacity: 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            ">
                <div style="
                    position: absolute;
                    top: -8px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 0;
                    height: 0;
                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                    border-bottom: 8px solid rgba(0, 0, 0, 0.85);
                "></div>
                <strong style="color: #4CAF50; font-size: 14px;">Required Fields:</strong><br>
                <div style="margin-top: 8px;">
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>Full Name</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>Email Address</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>Contact Number</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>At least one Target Position</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>At least one Preferred Location</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>At least one Skill</span>
                    </div>
                    <div style="display: flex; align-items: center; margin: 4px 0;">
                        <span style="color: #FF6B6B; margin-right: 8px;">•</span>
                        <span>At least one Job Type</span>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        function showTooltip() {
            const tooltip = document.getElementById('infoTooltip');
            const button = document.getElementById('infoButton');
            const overlay = document.getElementById('hoverOverlay');
            
            // Show tooltip with smooth animation
            tooltip.style.display = 'block';
            setTimeout(() => {
                tooltip.style.transform = 'translateY(0)';
                tooltip.style.opacity = '1';
            }, 10);
            
            // Add hover effects to button
            button.style.background = 'rgba(31, 119, 180, 0.95)';
            button.style.borderColor = 'rgba(255, 255, 255, 0.5)';
            button.style.transform = 'scale(1.1)';
            button.style.boxShadow = '0 4px 15px rgba(31, 119, 180, 0.4)';
            
            // Show overlay effect
            overlay.style.opacity = '1';
        }
        
        function hideTooltip() {
            const tooltip = document.getElementById('infoTooltip');
            const button = document.getElementById('infoButton');
            const overlay = document.getElementById('hoverOverlay');
            
            // Hide tooltip with smooth animation
            tooltip.style.transform = 'translateY(-10px)';
            tooltip.style.opacity = '0';
            
            setTimeout(() => {
                tooltip.style.display = 'none';
            }, 300);
            
            // Reset button effects
            button.style.background = 'rgba(31, 119, 180, 0.8)';
            button.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            button.style.transform = 'scale(1)';
            button.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
            
            // Hide overlay effect
            overlay.style.opacity = '0';
        }
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def custom_input_with_add_button(
        label: str,
        placeholder: str,
        key: str,
        add_button_key: str,
        add_callback: Callable,
        help_text: str = ""
    ):
        """Create custom input field with add button."""
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_input = st.text_input(
                label,
                placeholder=placeholder,
                key=key,
                help=help_text
            )
        with col2:
            if st.button("➕ Add", key=add_button_key, help=f"Add the {label.lower()}"):
                if custom_input and custom_input.strip():
                    add_callback(custom_input.strip())
                    st.rerun()
                else:
                    st.warning("Please enter a value!")
        
        return custom_input


class MultiselectWithCustom:
    """Enhanced multiselect component with custom input support."""
    
    @staticmethod
    def create_multiselect_with_custom(
        label: str,
        options: List[str],
        default_values: List[str],
        key: str,
        custom_input_key: str,
        add_button_key: str,
        add_callback: Callable,
        max_selections: Optional[int] = None,
        help_text: str = ""
    ) -> List[str]:
        """
        Create multiselect with custom input support.
        
        Args:
            label: Label for the multiselect
            options: Available options
            default_values: Default selected values
            key: Unique key for the multiselect
            custom_input_key: Key for custom input
            add_button_key: Key for add button
            add_callback: Callback function for adding custom values
            max_selections: Maximum number of selections allowed
            help_text: Help text for the component
            
        Returns:
            List of selected values
        """
        # Combine options with default values to ensure all selected items are available
        all_options = list(set(options + default_values))
        
        # Initialize session state if not exists
        if key not in st.session_state:
            st.session_state[key] = default_values
        
        # Get current values from session state
        current_values = st.session_state[key]
        
        # Filter current values to ensure they are valid options
        valid_current_values = [val for val in current_values if val in all_options]
        
        # Use a simpler approach - no default parameter to avoid conflicts
        selected_values = st.multiselect(
            label,
            options=all_options,
            key=f"{key}_multiselect",
            help=help_text
        )
        
        # If no values selected but we have valid current values, use them
        if not selected_values and valid_current_values:
            selected_values = valid_current_values
        
        # Update the main session state
        st.session_state[key] = selected_values
        
        # Custom input section
        # Clean the label by removing asterisk, HTML tags, and trailing colons
        clean_label = label.replace(" *", "").replace("<span style='color: red;'>*</span>", "").strip()
        clean_label = clean_label.rstrip(":")
        FormComponents.custom_input_with_add_button(
            label=f"Add custom {clean_label.lower()}:",
            placeholder=f"e.g., Custom {clean_label.lower()}",
            key=custom_input_key,
            add_button_key=add_button_key,
            add_callback=add_callback,
            help_text=f"Enter a custom {clean_label.lower()} not in the list above"
        )
        
        # Enforce max selections if specified
        if max_selections and len(selected_values) > max_selections:
            st.error(f"You can only select up to {max_selections} {label.lower()}.")
            selected_values = selected_values[:max_selections]
        
        return selected_values


class DisplayComponents:
    """Components for displaying data and results."""
    
    @staticmethod
    def display_personal_details(personal_details: dict):
        """Display personal details in a formatted way."""
        st.markdown("### Personal Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value=personal_details.get('full_name', ''), key='full_name_input')
        with col2:
            st.text_input("Contact Number", value=personal_details.get('contact', ''), key='contact_input')
        
        st.text_input("Email Address", value=personal_details.get('email', ''), key='email_input')
    
    @staticmethod
    def display_analysis_results(results: dict):
        """Display analysis results in a formatted way."""
        if not results:
            st.warning("No analysis results available.")
            return
        
        st.markdown("### Analysis Results")
        
        # Display extracted information
        if 'name' in results:
            st.success(f"✅ Extracted Name: {results['name']}")
        
        if 'phone' in results:
            st.info(f"📞 Phone: {results['phone']}")
        
        if 'email' in results:
            st.info(f"📧 Email: {results['email']}")
        
        if 'preferred_location' in results:
            st.info(f"📍 Primary Location: {results['preferred_location']}")
        
        # Display position matches
        if 'position_matches' in results:
            st.markdown("### Position Match Scores")
            for position, score in results['position_matches'].items():
                st.metric(position, f"{score}%")
    
    @staticmethod
    def display_extracted_links(links_data: dict):
        """Display extracted links from resume in a formatted way."""
        if not links_data or not any(links_data.values()):
            return
        
        st.markdown("### 🔗 Extracted Links from Resume")
        
        # Display GitHub links
        if links_data.get('github', {}).get('profile') or links_data.get('github', {}).get('project'):
            st.markdown("**GitHub:**")
            for profile in links_data['github'].get('profile', []):
                st.markdown(f"  - Profile: [{profile}]({profile})")
            for project in links_data['github'].get('project', []):
                st.markdown(f"  - Project: [{project}]({project})")
        
        # Display LinkedIn links
        if links_data.get('linkedin', {}).get('profile'):
            st.markdown("**LinkedIn:**")
            for profile in links_data['linkedin']['profile']:
                st.markdown(f"  - [{profile}]({profile})")
        
        # Display Portfolio links
        if links_data.get('portfolio'):
            st.markdown("**Portfolio:**")
            for portfolio in links_data['portfolio']:
                st.markdown(f"  - [{portfolio}]({portfolio})")
        
        # Display Email links
        if links_data.get('email'):
            st.markdown("**Email:**")
            for email in links_data['email']:
                st.markdown(f"  - {email}")
        
        # Display Other links
        if links_data.get('other'):
            st.markdown("**Other Links:**")
            for link in links_data['other']:
                st.markdown(f"  - [{link}]({link})")
    
    @staticmethod
    def display_job_recommendations(recommendations: List[dict]):
        """Display job recommendations in a formatted way."""
        if not recommendations:
            st.info("No job recommendations available.")
            return
        
        st.markdown("### 🎯 Job Recommendations")
        st.markdown("---")
        
        for i, job in enumerate(recommendations, 1):
            # Create job card with embedded URL in title
            job_title_with_url = f"[{job.get('title', 'Unknown Position')}]({job.get('application_url', '#')})"
            
            with st.container():
                st.markdown(f"#### {i}. {job_title_with_url}")
                
                # Job header with key info
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**🏢 {job.get('company', 'Unknown Company')}**")
                    st.markdown(f"📍 {job.get('location', 'N/A')}")
                
                with col2:
                    st.markdown(f"**💰 {job.get('salary_range', 'N/A')}**")
                
                with col3:
                    st.markdown(f"**📅 Posted: {job.get('date_posted', 'N/A')}**")
                
                with col4:
                    if 'match_score' in job:
                        match_score = job['match_score']
                        if isinstance(match_score, float):
                            match_score = f"{match_score:.0%}"
                        elif isinstance(match_score, str) and match_score.endswith('%'):
                            pass  # Already formatted
                        else:
                            match_score = f"{match_score}%"
                        
                        # Color code the match score
                        score_value = float(match_score.replace('%', ''))
                        if score_value >= 90:
                            color = "🟢"
                        elif score_value >= 80:
                            color = "🟡"
                        else:
                            color = "🟠"
                        
                        st.markdown(f"**{color} Match: {match_score}**")
                
                # Job ID
                if 'job_id' in job:
                    st.caption(f"Job ID: {job['job_id']}")
                
                # Description
                if 'description' in job and job['description']:
                    st.markdown("**📝 Description:**")
                    st.write(job['description'])
                
                # Requirements and Benefits in columns
                col_req, col_ben = st.columns(2)
                
                with col_req:
                    if 'requirements' in job and job['requirements']:
                        st.markdown("**📋 Requirements:**")
                        for req in job['requirements']:
                            st.write(f"• {req}")
                
                with col_ben:
                    if 'benefits' in job and job['benefits']:
                        st.markdown("**🎁 Benefits:**")
                        for benefit in job['benefits']:
                            st.write(f"• {benefit}")
                
                # Apply button
                if 'application_url' in job and job['application_url']:
                    st.markdown(f"[🔗 Apply for this position]({job['application_url']})")
                
                st.markdown("---")


class ReviewSection:
    """Review section component for the sidebar."""
    
    @staticmethod
    def display_review_section():
        """Display the review section in the sidebar."""
        st.markdown("### ⭐ Reviews & Feedback")
        st.markdown("---")
        
        # Sample reviews data
        reviews = [
            {
                "name": "Sarah Chen",
                "rating": 5,
                "comment": "CVLens helped me land my dream job! The AI analysis was spot-on.",
                "role": "Software Engineer"
            },
            {
                "name": "Michael Rodriguez",
                "rating": 5,
                "comment": "Amazing platform! Got 3 job offers within a week.",
                "role": "Data Scientist"
            },
            {
                "name": "Emily Johnson",
                "rating": 4,
                "comment": "Great resume tips and job matching. Highly recommended!",
                "role": "Marketing Manager"
            },
            {
                "name": "David Kim",
                "rating": 5,
                "comment": "The personalized recommendations are incredible. Game changer!",
                "role": "Product Manager"
            }
        ]
        
        # Display reviews
        for review in reviews:
            with st.container():
                # Review header
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{review['name']}**")
                    st.caption(f"{review['role']}")
                with col2:
                    # Star rating
                    stars = "⭐" * review['rating']
                    st.markdown(f"<div style='text-align: right; font-size: 14px;'>{stars}</div>", unsafe_allow_html=True)
                
                # Review comment
                st.markdown(f"*\"{review['comment']}\"*")
                st.markdown("---")
        
        # Add review button
        if st.button("📝 Leave a Review", use_container_width=True, key="leave_review_btn"):
            st.session_state.show_review_modal = True
            st.rerun()
        
        # Review modal
        if st.session_state.get('show_review_modal', False):
            ReviewSection.show_review_modal()
    
    @staticmethod
    def show_review_modal():
        """Show the review submission modal."""
        st.markdown("### 📝 Leave Your Review")
        
        with st.form("review_form"):
            # User details
            col1, col2 = st.columns(2)
            with col1:
                reviewer_name = st.text_input("Your Name", placeholder="Enter your name")
            with col2:
                reviewer_role = st.text_input("Your Role", placeholder="e.g., Software Engineer")
            
            # Rating
            rating = st.selectbox("Rating", options=[5, 4, 3, 2, 1], format_func=lambda x: "⭐" * x)
            
            # Review comment
            review_comment = st.text_area(
                "Your Review", 
                placeholder="Share your experience with CVLens...",
                height=100
            )
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Submit Review", type="primary"):
                    if reviewer_name and review_comment:
                        # Here you would typically save to a database
                        st.success("Thank you for your review! 🎉")
                        st.session_state.show_review_modal = False
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_review_modal = False
                    st.rerun()


class SessionStateManager:
    """Manages Streamlit session state initialization and updates."""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables."""
        if 'raw_resume_text' not in st.session_state:
            st.session_state.raw_resume_text = ""
        
        if 'full_name' not in st.session_state:
            st.session_state.full_name = ""
        
        if 'contact' not in st.session_state:
            st.session_state.contact = ""
        
        if 'email' not in st.session_state:
            st.session_state.email = ""
        
        if 'preferred_locations' not in st.session_state:
            st.session_state.preferred_locations = []
        
        if 'target_positions' not in st.session_state:
            st.session_state.target_positions = []
        
        if 'selected_job_types' not in st.session_state:
            st.session_state.selected_job_types = []
        
        if 'selected_job_level' not in st.session_state:
            st.session_state.selected_job_level = ""
        
        if 'skills' not in st.session_state:
            st.session_state.skills = []
        
        if 'analyzed_data' not in st.session_state:
            st.session_state.analyzed_data = None
        
        if 'backend_data' not in st.session_state:
            st.session_state.backend_data = None
        
        if 'is_analyzing' not in st.session_state:
            st.session_state.is_analyzing = False
        
        if 'extracted_single_location' not in st.session_state:
            st.session_state.extracted_single_location = ""
        
        if 'extracted_links' not in st.session_state:
            st.session_state.extracted_links = {}
        
        if 'show_review_modal' not in st.session_state:
            st.session_state.show_review_modal = False
    
    @staticmethod
    def update_session_state_from_analysis(analysis_data: dict):
        """Update session state with analysis results."""
        if not analysis_data:
            return
        
        # Update personal details
        if 'name' in analysis_data:
            st.session_state.full_name = analysis_data['name']
        
        if 'phone' in analysis_data:
            st.session_state.contact = analysis_data['phone']
        
        if 'email' in analysis_data:
            st.session_state.email = analysis_data['email']
        
        # Update location (only update the extracted location, don't modify user selections)
        if 'preferred_location' in analysis_data:
            extracted_loc = analysis_data['preferred_location']
            st.session_state.extracted_single_location = extracted_loc
            
            # Only add to preferred locations if user hasn't selected any locations yet
            # This preserves user's manual selections
            if not st.session_state.preferred_locations and extracted_loc != "Not specified":
                st.session_state.preferred_locations = [extracted_loc]
