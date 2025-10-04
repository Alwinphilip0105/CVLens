#!/usr/bin/env python3
"""
Script to access webhook response from terminal.
This script shows you how to get the webhook response data.
"""

import json
import os
import sys

def get_webhook_response_from_file():
    """Get webhook response from the exported data file."""
    try:
        # Check if user_data_export.json exists
        if os.path.exists('user_data_export.json'):
            with open('user_data_export.json', 'r') as f:
                data = json.load(f)
            
            print("=" * 80)
            print("📄 EXPORTED USER DATA")
            print("=" * 80)
            print(json.dumps(data, indent=2))
            print("=" * 80)
            return data
        else:
            print("❌ user_data_export.json not found")
            return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def simulate_webhook_response():
    """Simulate what a webhook response would look like."""
    print("=" * 80)
    print("🔗 SIMULATED WEBHOOK RESPONSE")
    print("=" * 80)
    
    # Example webhook response structure
    webhook_response = {
        "success": True,
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "preferred_location": "New York, NY",
            "job_recommendations": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "location": "New York, NY",
                    "salary_range": "$80,000 - $120,000",
                    "match_score": 0.95,
                    "application_url": "https://example.com/apply"
                },
                {
                    "title": "Data Scientist",
                    "company": "Data Inc",
                    "location": "San Francisco, CA",
                    "salary_range": "$90,000 - $130,000",
                    "match_score": 0.88,
                    "application_url": "https://example.com/apply2"
                }
            ]
        },
        "timestamp": "2025-01-04T13:48:37.865Z"
    }
    
    print(json.dumps(webhook_response, indent=2))
    print("=" * 80)
    return webhook_response

def show_webhook_access_methods():
    """Show different ways to access webhook response."""
    print("=" * 80)
    print("🎯 HOW TO ACCESS WEBHOOK RESPONSE FROM TERMINAL")
    print("=" * 80)
    print()
    print("1. 📱 RUN STREAMLIT APP:")
    print("   cd Frontend")
    print("   streamlit run streamlit_app.py")
    print("   # Then watch terminal for webhook logs")
    print()
    print("2. 🔍 CHECK EXPORTED DATA:")
    print("   python get_webhook_response.py")
    print()
    print("3. 📋 DIRECT PYTHON ACCESS:")
    print("   import json")
    print("   with open('user_data_export.json', 'r') as f:")
    print("       data = json.load(f)")
    print("       print(json.dumps(data, indent=2))")
    print()
    print("4. 🖥️ TERMINAL COMMANDS:")
    print("   # View exported data")
    print("   cat user_data_export.json")
    print("   # Pretty print JSON")
    print("   python -m json.tool user_data_export.json")
    print()
    print("=" * 80)

def main():
    """Main function."""
    print("🚀 WEBHOOK RESPONSE ACCESS TOOL")
    print("=" * 80)
    
    # Show access methods
    show_webhook_access_methods()
    
    # Try to get exported data
    print("\n📄 CHECKING FOR EXPORTED DATA...")
    exported_data = get_webhook_response_from_file()
    
    if exported_data:
        print("\n✅ Found exported user data!")
        print("📊 Summary:")
        print(f"   👤 Name: {exported_data.get('name', 'N/A')}")
        print(f"   📧 Email: {exported_data.get('email', 'N/A')}")
        print(f"   📞 Contact: {exported_data.get('contact', 'N/A')}")
        print(f"   🎯 Skills: {len(exported_data.get('skills', []))} found")
        print(f"   📍 Locations: {len(exported_data.get('location_preferences', []))} found")
    else:
        print("\n❌ No exported data found")
        print("💡 Run the Streamlit app and click 'Analyze Profile' to generate data")
    
    # Show example webhook response
    print("\n🔗 EXAMPLE WEBHOOK RESPONSE STRUCTURE:")
    simulate_webhook_response()
    
    print("\n🎯 TO GET REAL WEBHOOK RESPONSE:")
    print("1. Run: cd Frontend && streamlit run streamlit_app.py")
    print("2. Upload resume and click 'Analyze Profile'")
    print("3. Watch terminal for webhook communication logs")
    print("4. Check user_data_export.json for processed data")

if __name__ == "__main__":
    main()

