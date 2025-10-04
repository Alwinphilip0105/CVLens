#!/usr/bin/env python3
"""
Terminal webhook viewer - shows webhook response in real-time.
Run this in a separate terminal to watch webhook responses.
"""

import json
import time
import os
from datetime import datetime

def watch_webhook_logs():
    """Watch for webhook logs in real-time."""
    print("🔍 WEBHOOK RESPONSE TERMINAL VIEWER")
    print("=" * 60)
    print("📱 Instructions:")
    print("1. Keep this terminal open")
    print("2. Go to your browser and run the Streamlit app")
    print("3. Upload resume and click 'Analyze Profile'")
    print("4. Watch this terminal for webhook response")
    print("=" * 60)
    print("⏳ Waiting for webhook activity...")
    print("💡 Press Ctrl+C to stop")
    print()
    
    # Watch for changes in user_data_export.json
    last_modified = 0
    file_path = 'user_data_export.json'
    
    try:
        while True:
            if os.path.exists(file_path):
                current_modified = os.path.getmtime(file_path)
                
                if current_modified > last_modified:
                    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Data updated!")
                    
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        print("📥 WEBHOOK RESPONSE DATA:")
                        print("-" * 50)
                        print(f"👤 Name: {data.get('name', 'N/A')}")
                        print(f"📧 Email: {data.get('email', 'N/A')}")
                        print(f"📞 Contact: {data.get('contact', 'N/A')}")
                        print(f"🎯 Skills: {len(data.get('skills', []))} found")
                        print(f"📍 Locations: {data.get('location_preferences', [])}")
                        print(f"💼 Job Types: {data.get('job_types', [])}")
                        print(f"🎯 Preferences: {data.get('job_preferences', [])}")
                        print("-" * 50)
                        print("📋 Full Response:")
                        print(json.dumps(data, indent=2))
                        print("=" * 60)
                        
                        last_modified = current_modified
                        
                    except Exception as e:
                        print(f"❌ Error reading file: {e}")
            
            time.sleep(1)  # Check every second
            
    except KeyboardInterrupt:
        print("\n👋 Stopped watching webhook responses")

def show_current_webhook_data():
    """Show current webhook response data."""
    file_path = 'user_data_export.json'
    
    if os.path.exists(file_path):
        print("📥 CURRENT WEBHOOK RESPONSE DATA:")
        print("=" * 60)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print("📋 Full Response:")
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
        print(f"   🎯 Preferences: {len(data.get('job_preferences', []))} found")
        
    else:
        print("❌ No webhook response data found")
        print("💡 Run the Streamlit app and click 'Analyze Profile' first")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'watch':
        watch_webhook_logs()
    else:
        show_current_webhook_data()
        print("\n💡 To watch for real-time webhook responses:")
        print("   python terminal_webhook_viewer.py watch")

if __name__ == "__main__":
    main()

