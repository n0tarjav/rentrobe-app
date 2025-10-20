#!/usr/bin/env python3
import requests
import json

# Test session management
base_url = "http://localhost:5000"

def test_session_flow():
    """Test complete session flow"""
    print("=== TESTING SESSION FLOW ===")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test registration
    print("1. Testing registration...")
    user_data = {
        "name": "Session Test User",
        "email": "session@example.com",
        "password": "password123",
        "phone": "+91 9876543210",
        "city": "Mumbai"
    }
    
    try:
        response = session.post(f"{base_url}/api/auth/register", 
                              json=user_data,
                              headers={'Content-Type': 'application/json'})
        
        print(f"   Registration Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   User created: {data.get('user', {}).get('name')}")
        else:
            print(f"   Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Registration error: {e}")
        return False
    
    # Test profile access (should work if session is maintained)
    print("2. Testing profile access...")
    try:
        response = session.get(f"{base_url}/api/profile")
        print(f"   Profile Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Profile data: {data.get('name')} - {data.get('email')}")
            return True
        else:
            print(f"   Profile access failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Profile error: {e}")
        return False

def test_login_session():
    """Test login session flow"""
    print("\n=== TESTING LOGIN SESSION FLOW ===")
    
    # Create a session
    session = requests.Session()
    
    # Test login
    print("1. Testing login...")
    login_data = {
        "email": "demo@wearhouse.com",
        "password": "password123"
    }
    
    try:
        response = session.post(f"{base_url}/api/auth/login",
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        print(f"   Login Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Login successful: {data.get('user', {}).get('name')}")
        else:
            print(f"   Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Login error: {e}")
        return False
    
    # Test profile access
    print("2. Testing profile access after login...")
    try:
        response = session.get(f"{base_url}/api/profile")
        print(f"   Profile Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Profile data: {data.get('name')} - {data.get('email')}")
            return True
        else:
            print(f"   Profile access failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Profile error: {e}")
        return False

if __name__ == "__main__":
    print("Testing session management...")
    
    # Test registration session
    reg_success = test_session_flow()
    
    # Test login session
    login_success = test_login_session()
    
    print(f"\n=== RESULTS ===")
    print(f"Registration Session: {'PASS' if reg_success else 'FAIL'}")
    print(f"Login Session: {'PASS' if login_success else 'FAIL'}")

