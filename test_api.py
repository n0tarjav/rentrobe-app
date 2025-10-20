#!/usr/bin/env python3
import requests
import json

# Test the API endpoints
base_url = "http://localhost:5000"

def test_register():
    """Test user registration"""
    print("=== TESTING REGISTRATION ===")
    
    # Test data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "+91 9876543210",
        "city": "Mumbai"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json=user_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"User created: {data.get('user', {}).get('name')}")
            return True
        else:
            print(f"Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n=== TESTING LOGIN ===")
    
    # Test with demo user
    login_data = {
        "email": "demo@wearhouse.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login",
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful: {data.get('user', {}).get('name')}")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Login error: {e}")
        return False

def test_login_with_new_user():
    """Test login with newly created user"""
    print("\n=== TESTING LOGIN WITH NEW USER ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login",
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful: {data.get('user', {}).get('name')}")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Login error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    # Test registration
    register_success = test_register()
    
    # Test login with demo user
    login_success = test_login()
    
    # Test login with new user
    new_user_login_success = test_login_with_new_user()
    
    print(f"\n=== RESULTS ===")
    print(f"Registration: {'PASS' if register_success else 'FAIL'}")
    print(f"Demo Login: {'PASS' if login_success else 'FAIL'}")
    print(f"New User Login: {'PASS' if new_user_login_success else 'FAIL'}")

