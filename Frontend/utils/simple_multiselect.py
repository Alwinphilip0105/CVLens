"""
Simple multiselect implementation using checkboxes to avoid Streamlit's multiselect issues.
"""

import streamlit as st
from typing import List, Optional


def simple_multiselect(
    label: str,
    options: List[str],
    default: List[str] = None,
    key: str = None,
    help: str = None,
    max_selections: Optional[int] = None
) -> List[str]:
    """
    Simple multiselect using checkboxes to avoid Streamlit's multiselect issues.
    
    Args:
        label: Label for the multiselect
        options: Available options
        default: Default selected values
        key: Unique key for the component
        help: Help text
        max_selections: Maximum number of selections allowed
        
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
    
    # Display label
    st.write(f"**{label}**")
    if help:
        st.caption(help)
    
    # Create compact selection bars using selectbox with multiple selection
    selected_values = []
    
    # Use a more compact approach with selectbox
    if len(options) <= 6:
        # For small lists, use checkboxes in a single row
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            with cols[i]:
                is_selected = option in current_selected
                checkbox_key = f"{key}_checkbox_{i}"
                checked = st.checkbox(
                    option,
                    value=is_selected,
                    key=checkbox_key
                )
                if checked:
                    selected_values.append(option)
    else:
        # For larger lists, use a more compact multiselect approach
        # Create a horizontal scrollable container
        st.markdown("""
        <style>
        .compact-selection {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }
        .selection-item {
            background: #f0f2f6;
            border: 1px solid #d1d5db;
            border-radius: 20px;
            padding: 4px 12px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        .selection-item:hover {
            background: #e5e7eb;
        }
        .selection-item.selected {
            background: #1f77b4;
            color: white;
            border-color: #1f77b4;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Use regular multiselect for now (more compact than checkboxes)
        selected_values = st.multiselect(
            "",
            options=options,
            default=current_selected,
            key=f"{key}_compact",
            label_visibility="collapsed"
        )
    
    # Enforce max selections
    if max_selections and len(selected_values) > max_selections:
        st.error(f"You can only select up to {max_selections} options.")
        selected_values = selected_values[:max_selections]
    
    # Update state
    st.session_state[state_key] = selected_values
    
    return selected_values


def simple_multiselect_with_custom_input(
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
    Simple multiselect with custom input support using checkboxes.
    
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
    
    # Use simple multiselect
    selected_values = simple_multiselect(
        label=label,
        options=all_options,
        default=default_values,
        key=key,
        help=help_text,
        max_selections=max_selections
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
    
    return selected_values
