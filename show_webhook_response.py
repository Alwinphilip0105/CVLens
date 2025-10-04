#!/usr/bin/env python3
"""
Script to show n8n webhook response format in terminal.
"""

import json
from datetime import datetime

def show_webhook_response_format():
    """Show what n8n webhook response looks like."""
    
    print("=" * 80)
    print("📥 n8n WEBHOOK RESPONSE FORMAT")
    print("=" * 80)
    print()
    print("When n8n webhook is ACTIVE, you'll see this in terminal:")
    print()
    print("=================================================================================")
    print("🚀 WEBHOOK REQUEST TO n8n")
    print("=================================================================================")
    print("📍 URL: https://ruhack.app.n8n.cloud/webhook/getdata")
    print("📦 Payload:")
    print(json.dumps({
        "resume_text": "John Doe\\nSoftware Engineer\\n5 years experience...",
        "personal_details": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "contact": "+1234567890"
        },
        "job_preferences": {
            "preferred_locations": ["New York, NY"],
            "target_positions": ["Software Engineer"],
            "job_types": ["Full Time"],
            "preferences": ["Remote Work"]
        },
        "timestamp": "2025-01-04T13:48:37.865Z"
    }, indent=2))
    print("---------------------------------------------------------------------------------")
    print("📥 WEBHOOK RESPONSE FROM n8n")
    print("---------------------------------------------------------------------------------")
    print("✅ Status Code: 200")
    print("📄 Response Headers: {'content-type': 'application/json'}")
    print("📋 Response Body:")
    print(json.dumps({
        "success": True,
        "data": {
            "name": "John Doe",
            "email": "john.doe@example.com",
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
    }, indent=2))
    print("=================================================================================")
    print()
    print("🎯 CURRENT STATUS:")
    print("❌ n8n webhook is NOT ACTIVE (404 error)")
    print("💡 To activate n8n webhook:")
    print("   1. Go to your n8n workflow")
    print("   2. Click 'Execute workflow' button")
    print("   3. Then try again")
    print()
    print("🔄 FALLBACK BEHAVIOR:")
    print("When n8n webhook fails, the app uses LOCAL ANALYSIS")
    print("You'll see this in terminal:")
    print("❌ Backend webhook failed: 404 - The requested webhook is not registered")
    print("🔄 Falling back to local analysis...")
    print("✅ Local analysis completed successfully")
    print()
    print("📄 EXPORTED DATA (from local analysis):")
    print("=" * 60)
    
    # Show current exported data
    try:
        with open('user_data_export.json', 'r') as f:
            data = json.load(f)
        print(json.dumps(data, indent=2))
    except:
        print("No exported data found")
    
    print("=" * 60)

if __name__ == "__main__":
    show_webhook_response_format()

