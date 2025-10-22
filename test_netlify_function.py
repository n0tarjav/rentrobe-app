#!/usr/bin/env python3
"""
Test script to test the Netlify function directly
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment
os.environ['DATABASE_URL'] = 'sqlite:///instance/wearhouse.db'
os.environ['SECRET_KEY'] = 'test-secret-key'

# Import the Netlify function
from netlify.functions.api import handler

def test_netlify_function():
    """Test the Netlify function with items endpoint"""
    try:
        # Create a mock event
        event = {
            'path': '/api/items',
            'httpMethod': 'GET',
            'headers': {},
            'body': '',
            'queryStringParameters': {}
        }
        
        context = {}
        
        print("Testing Netlify function...")
        print(f"Event: {event}")
        
        # Call the handler
        result = handler(event, context)
        
        print(f"Status Code: {result['statusCode']}")
        print(f"Headers: {result['headers']}")
        
        if result['statusCode'] == 200:
            try:
                # Check if body is already parsed or needs parsing
                if isinstance(result['body'], str):
                    data = json.loads(result['body'])
                else:
                    data = result['body']
                
                items = data.get('items', [])
                print(f"Number of items returned: {len(items)}")
                
                # Check for inactive items
                inactive_items = [item for item in items if item.get('is_active') == False]
                print(f"Number of inactive items: {len(inactive_items)}")
                
                if inactive_items:
                    print("Inactive items found:")
                    for item in inactive_items:
                        print(f"  - {item.get('title')} (ID: {item.get('id')})")
                else:
                    print("No inactive items found - filtering is working correctly!")
                    
                # Show first few items
                print(f"\nFirst 3 items:")
                for i, item in enumerate(items[:3]):
                    print(f"  {i+1}. {item.get('title')} - Active: {item.get('is_active', 'N/A')}")
                    
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error parsing response: {e}")
                print(f"Response body type: {type(result['body'])}")
                print(f"Response body: {result['body']}")
        else:
            print(f"Error: {result['body']}")
            
    except Exception as e:
        print(f"Error testing Netlify function: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import json
    test_netlify_function()