#!/usr/bin/env python3
"""
Real-time webhook response watcher.
This script shows you how to monitor webhook responses from terminal.
"""

import json
import time
import os
from datetime import datetime

def watch_webhook_response():
    """Watch for webhook response in real-time."""
    print("🔍 WEBHOOK RESPONSE WATCHER")
    print("=" * 60)
    print("📱 To get webhook response:")
    print("1. Run: cd Frontend && streamlit run streamlit_app.py")
    print("2. Upload resume and click 'Analyze Profile'")
    print("3. Watch this terminal for webhook logs")
    print("=" * 60)
    print("⏳ Waiting for webhook response...")
    print("💡 Press Ctrl+C to stop")
    print()
    
    last_modified = 0
    file_path = 'user_data_export.json'
    
    try:
        while True:
            if os.path.exists(file_path):
                current_modified = os.path.getmtime(file_path)
                
                if current_modified > last_modified:
                    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] File updated!")
                    
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        print("📄 NEW WEBHOOK DATA:")
                        print("-" * 40)
                        print(f"👤 Name: {data.get('name', 'N/A')}")
                        print(f"📧 Email: {data.get('email', 'N/A')}")
                        print(f"📞 Contact: {data.get('contact', 'N/A')}")
                        print(f"🎯 Skills: {len(data.get('skills', []))} found")
                        print(f"📍 Locations: {data.get('location_preferences', [])}")
                        print(f"💼 Job Types: {data.get('job_types', [])}")
                        print("-" * 40)
                        print("📋 Full JSON:")
                        print(json.dumps(data, indent=2))
                        print("=" * 60)
                        
                        last_modified = current_modified
                        
                    except Exception as e:
                        print(f"❌ Error reading file: {e}")
            
            time.sleep(1)  # Check every second
            
    except KeyboardInterrupt:
        print("\n👋 Stopped watching")

def show_current_data():
    """Show current exported data."""
    file_path = 'user_data_export.json'
    
    if os.path.exists(file_path):
        print("📄 CURRENT EXPORTED DATA:")
        print("=" * 60)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(json.dumps(data, indent=2))
        print("=" * 60)
        
        # Show summary
        print("📊 SUMMARY:")
        print(f"   👤 Name: {data.get('name', 'N/A')}")
        print(f"   📧 Email: {data.get('email', 'N/A')}")
        print(f"   📞 Contact: {data.get('contact', 'N/A')}")
        print(f"   🎯 Skills: {len(data.get('skills', []))} found")
        print(f"   📍 Locations: {len(data.get('location_preferences', []))} found")
        print(f"   💼 Job Types: {len(data.get('job_types', []))} found")
        
    else:
        print("❌ No exported data found")
        print("💡 Run the Streamlit app and click 'Analyze Profile' first")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'watch':
        watch_webhook_response()
    else:
        show_current_data()
        print("\n💡 To watch for real-time updates:")
        print("   python watch_webhook.py watch")

if __name__ == "__main__":
    main()

