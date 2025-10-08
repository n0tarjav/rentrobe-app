#!/usr/bin/env python3
import requests
import json

# Test frontend session handling
base_url = "http://localhost:5000"

def test_frontend_flow():
    """Test the exact flow that the frontend uses"""
    print("=== TESTING FRONTEND FLOW ===")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Register a user (like frontend does)
    print("1. Registering user...")
    user_data = {
        "name": "Frontend Test User",
        "email": "frontendtest@example.com",
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
            print(f"   Session cookies: {session.cookies.get_dict()}")
        else:
            print(f"   Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Registration error: {e}")
        return False
    
    # Step 2: Check profile immediately after registration (like frontend does)
    print("2. Checking profile immediately after registration...")
    try:
        response = session.get(f"{base_url}/api/profile")
        print(f"   Profile Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Profile data: {data.get('name')} - {data.get('email')}")
            print(f"   Session cookies: {session.cookies.get_dict()}")
            return True
        else:
            print(f"   Profile access failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Profile error: {e}")
        return False

def test_login_flow():
    """Test login flow"""
    print("\n=== TESTING LOGIN FLOW ===")
    
    # Create a new session
    session = requests.Session()
    
    # Step 1: Login
    print("1. Logging in...")
    login_data = {
        "email": "frontendtest@example.com",
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
            print(f"   Session cookies: {session.cookies.get_dict()}")
        else:
            print(f"   Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Login error: {e}")
        return False
    
    # Step 2: Check profile after login
    print("2. Checking profile after login...")
    try:
        response = session.get(f"{base_url}/api/profile")
        print(f"   Profile Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Profile data: {data.get('name')} - {data.get('email')}")
            print(f"   Session cookies: {session.cookies.get_dict()}")
            return True
        else:
            print(f"   Profile access failed: {response.text}")
            return False
    except Exception as e:
        print(f"   Profile error: {e}")
        return False

if __name__ == "__main__":
    print("Testing frontend session flow...")
    
    # Test registration flow
    reg_success = test_frontend_flow()
    
    # Test login flow
    login_success = test_login_flow()
    
    print(f"\n=== RESULTS ===")
    print(f"Registration Flow: {'PASS' if reg_success else 'FAIL'}")
    print(f"Login Flow: {'PASS' if login_success else 'FAIL'}")
