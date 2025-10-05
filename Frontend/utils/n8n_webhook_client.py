"""
N8N Webhook Client - Python equivalent of the JavaScript fetch code.
Handles direct communication with the n8n webhook endpoint.
"""

import requests
import json
from datetime import datetime
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
        
        # Alternative URLs to try if the main one fails
        self.alternative_urls = [
            "https://ruhack.app.n8n.cloud/webhook-test/getdata",
            "https://ruhack.app.n8n.cloud/webhook/getdata",
            "https://ruhack.app.n8n.cloud/webhook-test",
            "https://ruhack.app.n8n.cloud/webhook"
        ]
    
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
            import json
            json_data = json.dumps(user_data)
            
            # Print the data being sent (equivalent to console.log in JavaScript)
            print("\n" + "="*80)
            print("N8N WEBHOOK - SENDING DATA")
            print("="*80)
            print(f"URL: {self.webhook_url}")
            print(f"Data Size: {len(json_data)} characters")
            print(f"Complete Data Structure:")
            try:
                import json
                data_dict = json.loads(json_data)
                for key, value in data_dict.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"   {key}: {value[:100]}... ({len(value)} chars)")
                    elif isinstance(value, list):
                        print(f"   {key}: {value} (list with {len(value)} items)")
                    else:
                        print(f"   {key}: {value}")
                
                # Specifically check for the problematic fields
                print("\nSPECIFIC FIELD CHECK:")
                print(f"   target_positions: {data_dict.get('target_positions', 'NOT FOUND')}")
                print(f"   preferred_locations: {data_dict.get('preferred_locations', 'NOT FOUND')}")
                print(f"   skills: {data_dict.get('skills', 'NOT FOUND')}")
                print(f"   selected_job_types: {data_dict.get('selected_job_types', 'NOT FOUND')}")
                
            except Exception as e:
                print(f"   Error parsing data: {e}")
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
            print("RESPONSE FROM N8N WEBHOOK")
            print("-" * 80)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            print("=" * 80)
            
            # Check if request was successful
            if response.status_code == 200:
                try:
                    # Parse JSON response (equivalent to response.json() in JavaScript)
                    response_data = response.json()
                    print("✅ Successfully received data from n8n webhook!")
                    
                    # Validate that n8n received the key fields
                    if isinstance(response_data, dict):
                        print("🔍 N8N Response Validation:")
                        print(f"   Response keys: {list(response_data.keys())}")
                        if 'received_data' in response_data:
                            received = response_data['received_data']
                            print(f"   target_positions received: {received.get('target_positions', 'NOT FOUND')}")
                            print(f"   preferred_locations received: {received.get('preferred_locations', 'NOT FOUND')}")
                            print(f"   skills received: {received.get('skills', 'NOT FOUND')}")
                            print(f"   selected_job_types received: {received.get('selected_job_types', 'NOT FOUND')}")
                    
                    return response_data
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON response from webhook")
                    print(f"Raw response: {response.text}")
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
            print(f"Error: Unexpected error - {str(e)}")
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
    # Print all session state keys for debugging
    print("\n" + "="*80)
    print("DEBUGGING: All session state keys:")
    print("="*80)
    for key, value in session_state.items():
        print(f"Key: {key} | Type: {type(value).__name__} | Value: {str(value)[:100]}...")
    print("="*80)
    
    # Helper function to get form data with fallback to multiselect keys
    def get_form_data(key, multiselect_key=None):
        """Get form data with fallback to multiselect key"""
        value = session_state.get(key, [])
        if not value and multiselect_key:
            value = session_state.get(multiselect_key, [])
        return value if value else []
    
    # Extract data from session state (equivalent to getting data from form)
    user_data = {
        "resume_text": session_state.get('raw_resume_text', ''),
        "full_name": session_state.get('full_name', ''),
        "email": session_state.get('email', ''),
        "contact": session_state.get('contact', ''),
        "preferred_locations": get_form_data('preferred_locations', 'location_select'),
        "target_positions": get_form_data('target_positions', 'position_select'),
        "skills": get_form_data('skills', 'skill_select'),
        "selected_job_types": get_form_data('selected_job_types', 'job_type_select'),
        "selected_job_level": session_state.get('selected_job_level', ''),
        # Add additional fields that might be missing

        "resume_file_name": session_state.get('resume_file_name', ''),
        "resume_file_path": session_state.get('resume_file_path', ''),
        "timestamp": datetime.now().isoformat()
    }
    
    # Print the complete user_data being sent
    print("\n" + "="*80)
    print("DEBUGGING: Complete user_data being sent to n8n:")
    print("="*80)
    print(json.dumps(user_data, indent=2, default=str))
    print("="*80)
    
    # Create webhook client
    webhook_client = N8NWebhookClient()
    
    # Send data to webhook
    response_data = webhook_client.send_user_data(user_data)
    
    # Print response data
    print("\n" + "="*80)
    print("DEBUGGING: Response from n8n webhook:")
    print("="*80)
    print(json.dumps(response_data, indent=2, default=str) if response_data else "No response data")
    print("="*80)
    
    return response_data


def test_n8n_webhook() -> bool:
    """
    Test if the n8n webhook is accessible.
    
    Returns:
        True if webhook is accessible, False otherwise
    """
    try:
        webhook_client = N8NWebhookClient()
        
        print(f"Testing N8N webhook connectivity to: {webhook_client.webhook_url}")
        
        # First try a simple GET request to check if the endpoint is reachable
        try:
            import requests
            response = requests.get(webhook_client.webhook_url, timeout=10)
            print(f"GET request successful - Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        except Exception as get_error:
            print(f"GET request failed: {get_error}")
            print("This is normal for POST-only webhooks, continuing with POST test...")
        
        # Send test data with the specific fields that might be missing
        test_data = {
            "test": True,
            "message": "Testing n8n webhook connection",
            "timestamp": "2024-01-01T00:00:00Z",
            "target_positions": ["Software Engineer", "Data Scientist"],
            "preferred_locations": ["New York", "San Francisco"],
            "skills": ["Python", "Machine Learning"],
            "selected_job_types": ["Full-time", "Remote"]
        }
        
        print("Sending test data to N8N webhook...")
        response_data = webhook_client.send_user_data(test_data)
        
        if response_data:
            print("N8N webhook test successful!")
            return True
        else:
            print("N8N webhook test failed - no response data")
            return False
        
    except Exception as e:
        print(f"N8N webhook test failed: {str(e)}")
        import traceback
        print(f"Full error traceback: {traceback.format_exc()}")
        return False


def test_multiple_n8n_urls() -> Dict[str, bool]:
    """
    Test multiple N8N webhook URLs to find which one works.
    
    Returns:
        Dictionary mapping URLs to their success status
    """
    results = {}
    test_data = {"test": True, "message": "URL connectivity test"}
    
    urls_to_test = [
        "https://ruhack.app.n8n.cloud/webhook-test/getdata",
        "https://ruhack.app.n8n.cloud/webhook/getdata", 
        "https://ruhack.app.n8n.cloud/webhook-test",
        "https://ruhack.app.n8n.cloud/webhook",
        "https://ruhack.app.n8n.cloud/webhook-test/getdata/",
        "https://ruhack.app.n8n.cloud/webhook/getdata/"
    ]
    
    print("🔍 Testing multiple N8N webhook URLs...")
    
    for url in urls_to_test:
        try:
            print(f"\n🔄 Testing: {url}")
            client = N8NWebhookClient(url)
            
            # Try GET first
            try:
                response = requests.get(url, timeout=5)
                print(f"   GET Status: {response.status_code}")
                if response.status_code in [200, 405]:
                    results[url] = True
                    print(f"   ✅ GET successful")
                    continue
            except Exception as e:
                print(f"   ⚠️ GET failed: {e}")
            
            # Try POST
            try:
                response_data = client.send_user_data(test_data)
                if response_data:
                    results[url] = True
                    print(f"   ✅ POST successful")
                else:
                    results[url] = False
                    print(f"   ❌ POST failed - no response")
            except Exception as e:
                results[url] = False
                print(f"   ❌ POST failed: {e}")
                
        except Exception as e:
            results[url] = False
            print(f"   ❌ URL test failed: {e}")
    
    print(f"\n📊 URL Test Results:")
    for url, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {url}")
    
    return results


def send_test_data_to_n8n() -> Optional[Dict[str, Any]]:
    """
    Send test data with all form fields to n8n webhook for debugging.
    
    Returns:
        Response data from n8n webhook or None if failed
    """
    try:
        # Create webhook client
        webhook_client = N8NWebhookClient()
        
        # Send comprehensive test data
        test_data = {
            "resume_text": "Test resume text for debugging",
            "full_name": "Test User",
            "email": "test@example.com",
            "contact": "123-456-7890",
            "preferred_locations": ["New York", "San Francisco", "Remote"],
            "target_positions": ["Software Engineer", "Data Scientist", "Product Manager"],
            "skills": ["Python", "Machine Learning", "React", "SQL"],
            "selected_job_types": ["Full-time", "Remote", "Contract"],
            "test_mode": True,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        print("🧪 Sending test data to N8N webhook...")
        response_data = webhook_client.send_user_data(test_data)
        
        if response_data:
            print("✅ Test data sent successfully!")
            return response_data
        else:
            print("❌ Test data send failed!")
            return None
        
    except Exception as e:
        print(f"❌ Test data send failed: {str(e)}")
        return None


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
