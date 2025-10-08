#!/usr/bin/env python3
"""
Test script for Netlify function
"""

import json
import sys
from pathlib import Path

# Add the netlify functions directory to path
netlify_functions = Path(__file__).parent / 'netlify' / 'functions'
sys.path.insert(0, str(netlify_functions))

# Import the handler
from api import handler

def test_registration():
    """Test user registration"""
    print("=== TESTING REGISTRATION ===")
    
    event = {
        'path': '/api/auth/register',
        'httpMethod': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'name': 'Netlify Test User',
            'email': 'netlifytest@example.com',
            'password': 'password123',
            'phone': '+91 9876543210',
            'city': 'Mumbai'
        }),
        'queryStringParameters': None
    }
    
    context = {}
    
    try:
        result = handler(event, context)
        print(f"Status Code: {result['statusCode']}")
        print(f"Response: {result['body']}")
        return result['statusCode'] == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n=== TESTING LOGIN ===")
    
    event = {
        'path': '/api/auth/login',
        'httpMethod': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'email': 'netlifytest@example.com',
            'password': 'password123'
        }),
        'queryStringParameters': None
    }
    
    context = {}
    
    try:
        result = handler(event, context)
        print(f"Status Code: {result['statusCode']}")
        print(f"Response: {result['body']}")
        return result['statusCode'] == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_profile():
    """Test profile access"""
    print("\n=== TESTING PROFILE ===")
    
    event = {
        'path': '/api/profile',
        'httpMethod': 'GET',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '',
        'queryStringParameters': None
    }
    
    context = {}
    
    try:
        result = handler(event, context)
        print(f"Status Code: {result['statusCode']}")
        print(f"Response: {result['body']}")
        return result['statusCode'] == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Netlify function...")
    
    # Test registration
    reg_success = test_registration()
    
    # Test login
    login_success = test_login()
    
    # Test profile
    profile_success = test_profile()
    
    print(f"\n=== RESULTS ===")
    print(f"Registration: {'PASS' if reg_success else 'FAIL'}")
    print(f"Login: {'PASS' if login_success else 'FAIL'}")
    print(f"Profile: {'PASS' if profile_success else 'FAIL'}")
    
    if all([reg_success, login_success, profile_success]):
        print("\n[SUCCESS] All tests passed! Ready for Netlify deployment!")
    else:
        print("\n[ERROR] Some tests failed. Check the errors above.")
