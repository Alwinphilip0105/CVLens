#!/usr/bin/env python3
"""
Main entry point for the RU Hack Frontend application.
This module provides different ways to run the Streamlit application.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_streamlit_app():
    """Run the Streamlit app directly."""
    print("Starting RU Hack Frontend Application...")
    print("The Streamlit app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    # Get the directory where this script is located
    frontend_dir = Path(__file__).parent
    streamlit_app_path = frontend_dir / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"Error: streamlit_app.py not found in {frontend_dir}")
        return False
    
    try:
        # Change to the frontend directory and run streamlit
        os.chdir(frontend_dir)
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
        return True
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")
        return False
    except FileNotFoundError:
        print("Error: Python or Streamlit not found. Please install Streamlit: pip install streamlit")
        return False

def run_with_poetry():
    """Run the Streamlit app using Poetry."""
    print("Starting RU Hack Frontend Application with Poetry...")
    
    frontend_dir = Path(__file__).parent
    streamlit_app_path = frontend_dir / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"Error: streamlit_app.py not found in {frontend_dir}")
        return False
    
    try:
        # Change to the project root directory for Poetry
        project_root = frontend_dir.parent
        os.chdir(project_root)
        
        # Run with Poetry
        subprocess.run([
            sys.executable, "-m", "poetry", "run", 
            "python", "-m", "streamlit", "run", 
            str(streamlit_app_path)
        ], check=True)
        return True
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running with Poetry: {e}")
        print("Trying direct method...")
        return run_streamlit_app()
    except FileNotFoundError:
        print("Error: Poetry not found. Trying direct method...")
        return run_streamlit_app()

def show_help():
    """Show help information."""
    print("""
RU Hack Frontend Application

Usage:
    python main.py [option]

Options:
    direct, d     Run Streamlit directly (default)
    poetry, p     Run using Poetry
    help, h       Show this help message

Examples:
    python main.py              # Run directly
    python main.py direct       # Run directly
    python main.py poetry       # Run with Poetry
    python main.py help         # Show help

The application will open in your browser at http://localhost:8501
""")

def main():
    """Main function with command line argument handling."""
    if len(sys.argv) > 1:
        option = sys.argv[1].lower()
        
        if option in ['help', 'h', '-h', '--help']:
            show_help()
            return
        elif option in ['poetry', 'p']:
            success = run_with_poetry()
        elif option in ['direct', 'd']:
            success = run_streamlit_app()
        else:
            print(f"Unknown option: {option}")
            show_help()
            return
    else:
        # Default: try direct method
        success = run_streamlit_app()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
