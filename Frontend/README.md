# RU Hack Frontend

This is the frontend application for the RU Hack project, built with Streamlit.

## Files

- `main.py` - Main entry point with multiple run options
- `streamlit_app.py` - The main Streamlit application
- `run_app.py` - Simple script to run the Streamlit app
- `__init__.py` - Package initialization

## Quick Start

### Option 1: Using main.py (Recommended)
```bash
# Run directly (default)
python main.py

# Run with Poetry
python main.py poetry

# Show help
python main.py help
```

### Option 2: Using run_app.py
```bash
python run_app.py
```

### Option 3: Direct Streamlit
```bash
python -m streamlit run streamlit_app.py
```

## Features

The Streamlit app includes:
- Interactive web interface
- Data visualization
- File upload functionality
- Multiple pages with navigation
- Responsive design

## Requirements

- Python 3.12+
- Streamlit
- Other dependencies as specified in the main project's pyproject.toml

## Development

The app will open in your browser at `http://localhost:8501` when running.
