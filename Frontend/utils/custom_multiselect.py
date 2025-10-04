"""
Custom multiselect component that handles selection state properly.
"""

import streamlit as st
from typing import List, Optional


def custom_multiselect(
    label: str,
    options: List[str],
    default: List[str] = None,
    key: str = None,
    help: str = None
) -> List[str]:
    """
    Custom multiselect that handles state properly to avoid first-click issues.
    
    Args:
        label: Label for the multiselect
        options: Available options
        default: Default selected values
        key: Unique key for the component
        help: Help text
        
    Returns:
        List of selected values
    """
    if default is None:
        default = []
    
    if key is None:
        key = f"multiselect_{hash(label)}"
    
    # Initialize session state
    state_key = f"{key}_state"
    if state_key not in st.session_state:
        st.session_state[state_key] = default
    
    # Get current state
    current_selected = st.session_state[state_key]
    
    # Create the multiselect without default parameter
    selected = st.multiselect(
        label,
        options=options,
        key=f"{key}_widget",
        help=help
    )
    
    # If no selection made, use current values
    if not selected and current_selected:
        selected = current_selected
    
    # Update state
    st.session_state[state_key] = selected
    
    return selected


def custom_multiselect_with_custom_input(
    label: str,
    options: List[str],
    default_values: List[str] = None,
    key: str = None,
    custom_input_key: str = None,
    add_button_key: str = None,
    add_callback=None,
    max_selections: Optional[int] = None,
    help_text: str = ""
) -> List[str]:
    """
    Custom multiselect with custom input support that handles state properly.
    
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
    if default_values is None:
        default_values = []
    
    if key is None:
        key = f"multiselect_{hash(label)}"
    
    # Combine options with default values to ensure all selected items are available
    all_options = list(set(options + default_values))
    
    # Use custom multiselect
    selected_values = custom_multiselect(
        label=label,
        options=all_options,
        default=default_values,
        key=key,
        help=help_text
    )
    
    # Custom input section
    if custom_input_key and add_button_key and add_callback:
        # Clean the label by removing asterisk, HTML tags, and trailing colons
        clean_label = label.replace(" *", "").replace("<span style='color: red;'>*</span>", "").strip()
        clean_label = clean_label.rstrip(":")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_input = st.text_input(
                f"Add custom {clean_label.lower()}:",
                placeholder=f"e.g., Custom {clean_label.lower()}",
                key=custom_input_key,
                help=f"Enter a custom {clean_label.lower()} not in the list above"
            )
        with col2:
            if st.button("➕ Add", key=add_button_key, help=f"Add the {clean_label.lower()}"):
                if custom_input and custom_input.strip():
                    add_callback(custom_input.strip())
                    st.rerun()
                else:
                    st.warning("Please enter a value!")
    
    # Enforce max selections if specified
    if max_selections and len(selected_values) > max_selections:
        st.error(f"You can only select up to {max_selections} {label.lower()}.")
        selected_values = selected_values[:max_selections]
    
    return selected_values
