"""
N8N Webhook Client - Python equivalent of the JavaScript fetch code.
Handles direct communication with the n8n webhook endpoint.
"""

import requests
import json
from typing import Dict, Any, Optional
import streamlit as st


class N8NWebhookClient:
    """Client for communicating with n8n webhook endpoints."""
    
    def __init__(self, webhook_url: str = "https://ruhack.app.n8n.cloud/webhook-test/getdata"):
        """
        Initialize the n8n webhook client.
        
        Args:
            webhook_url: The n8n webhook URL
        """
        self.webhook_url = webhook_url
        self.timeout = 30  # seconds
    
    def send_user_data(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send user data to n8n webhook (Python equivalent of the JavaScript fetch).
        
        Args:
            user_data: Dictionary containing user data (resume_text, full_name, email, etc.)
            
        Returns:
            Response data from n8n webhook or None if failed
        """
        try:
            # Convert data to JSON (equivalent to JSON.stringify in JavaScript)
            json_data = json.dumps(user_data)
            
            # Print the data being sent (equivalent to console.log in JavaScript)
            print("\n" + "="*80)
            print("🚀 N8N WEBHOOK - SENDING DATA")
            print("="*80)
            print(f"📍 URL: {self.webhook_url}")
            print(f"📦 Data Size: {len(json_data)} characters")
            print(f"📋 Data Preview:")
            try:
                import json
                data_dict = json.loads(json_data)
                for key, value in data_dict.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"   {key}: {value[:100]}... ({len(value)} chars)")
                    else:
                        print(f"   {key}: {value}")
            except:
                print(f"   Raw data: {json_data[:200]}...")
            print("-" * 80)
            
            # Send POST request (equivalent to fetch with POST method)
            response = requests.post(
                self.webhook_url,
                headers={
                    "Content-Type": "application/json"
                },
                data=json_data,
                timeout=self.timeout
            )
            
            # Print response details (equivalent to console.log in JavaScript)
            print("📥 RESPONSE FROM N8N WEBHOOK")
            print("-" * 80)
            print(f"✅ Status Code: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            print(f"📋 Response Body: {response.text}")
            print("=" * 80)
            
            # Check if request was successful
            if response.status_code == 200:
                try:
                    # Parse JSON response (equivalent to response.json() in JavaScript)
                    response_data = response.json()
                    print("✅ Successfully received data from n8n webhook!")
                    return response_data
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON response from webhook")
                    return None
            else:
                print(f"❌ Error: HTTP {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Error: Request timeout - webhook took too long to respond")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Error: Connection error - unable to reach webhook")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: Request failed - {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error: Unexpected error - {str(e)}")
            return None


def send_static_data_to_n8n() -> Optional[Dict[str, Any]]:
    """
    Send static data to n8n webhook (exact equivalent of the JavaScript code).
    This function replicates the JavaScript code you provided.
    
    Returns:
        Response data from n8n webhook or None if failed
    """
    # Static user data (equivalent to the JavaScript userData object)
    user_data = {
        "resume_text": "Alwin Philip Camden ...",
        "full_name": "Alwin Philip", 
        "email": "alwinphilip0105@gmail.com"
    }
    
    # Create webhook client
    webhook_client = N8NWebhookClient()
    
    # Send data to webhook
    response_data = webhook_client.send_user_data(user_data)
    
    return response_data


def send_dynamic_data_to_n8n(session_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Send dynamic data from Streamlit session state to n8n webhook.
    
    Args:
        session_state: Streamlit session state containing user data
        
    Returns:
        Response data from n8n webhook or None if failed
    """
    # Extract data from session state (equivalent to getting data from form)
    user_data = {
        "resume_text": session_state.get('raw_resume_text', ''),
        "full_name": session_state.get('full_name', ''),
        "email": session_state.get('email', ''),
        "contact": session_state.get('contact', ''),
        "preferred_locations": session_state.get('preferred_locations', []),
        "target_positions": session_state.get('target_positions', []),
        "skills": session_state.get('skills', []),
        "selected_job_types": session_state.get('selected_job_types', [])
    }
    
    # Create webhook client
    webhook_client = N8NWebhookClient()
    
    # Send data to webhook
    response_data = webhook_client.send_user_data(user_data)
    
    return response_data


def test_n8n_webhook() -> bool:
    """
    Test if the n8n webhook is accessible.
    
    Returns:
        True if webhook is accessible, False otherwise
    """
    try:
        webhook_client = N8NWebhookClient()
        
        # Test with a simple GET request
        response = requests.get(webhook_client.webhook_url, timeout=5)
        
        # 200 OK or 405 Method Not Allowed are both acceptable for webhooks
        return response.status_code in [200, 405]
    except:
        return False


# Example usage functions
def example_static_data():
    """Example of sending static data (matches your JavaScript code exactly)."""
    print("Testing n8n webhook with static data...")
    response = send_static_data_to_n8n()
    
    if response:
        print("✅ Success! Response from n8n:")
        print(json.dumps(response, indent=2))
    else:
        print("❌ Failed to get response from n8n webhook")


def example_dynamic_data():
    """Example of sending dynamic data from Streamlit session state."""
    # This would be called from within your Streamlit app
    # with the actual session state
    pass


if __name__ == "__main__":
    # Test the webhook connection
    print("Testing n8n webhook connection...")
    if test_n8n_webhook():
        print("✅ Webhook is accessible!")
        example_static_data()
    else:
        print("❌ Webhook is not accessible!")
