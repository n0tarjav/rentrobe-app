#!/usr/bin/env python3
"""
Test script to debug Netlify login issues
"""

import requests
import json

def test_netlify_login():
    """Test login on Netlify deployment"""
    
    # Replace with your actual Netlify URL
    base_url = "https://your-site-name.netlify.app"
    
    # Test credentials
    test_credentials = [
        {
            "email": "demo@wearhouse.com",
            "password": "password123"
        },
        {
            "email": "arjav@rentrobe.com", 
            "password": "arjav0302"
        }
    ]
    
    print("Testing Netlify login...")
    print(f"Base URL: {base_url}")
    
    for creds in test_credentials:
        print(f"\n--- Testing login for {creds['email']} ---")
        
        try:
            response = requests.post(
                f"{base_url}/api/auth/login",
                json=creds,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            try:
                response_data = response.json()
                print(f"Response Data: {json.dumps(response_data, indent=2)}")
            except:
                print(f"Response Text: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Test database status
    print(f"\n--- Testing database status ---")
    try:
        response = requests.get(f"{base_url}/api/test", timeout=30)
        print(f"Database Test Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Database Test Response: {response.json()}")
        else:
            print(f"Database Test Error: {response.text}")
    except Exception as e:
        print(f"Database Test Error: {e}")

if __name__ == "__main__":
    test_netlify_login()
