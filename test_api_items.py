#!/usr/bin/env python3
"""
Test script to verify that the API is working correctly and filtering out inactive items
"""

import requests
import json

def test_api_items():
    """Test the /api/items endpoint"""
    try:
        # Test the API endpoint
        response = requests.get('http://localhost:5000/api/items')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of items returned: {len(data.get('items', []))}")
            
            # Check if any items have is_active = False
            items = data.get('items', [])
            inactive_items = [item for item in items if item.get('is_active') == False]
            print(f"Number of inactive items: {len(inactive_items)}")
            
            if inactive_items:
                print("Inactive items found:")
                for item in inactive_items:
                    print(f"  - {item.get('title')} (ID: {item.get('id')})")
            else:
                print("No inactive items found - filtering is working correctly!")
                
            # Print first few items for verification
            print("\nFirst 3 items:")
            for i, item in enumerate(items[:3]):
                print(f"  {i+1}. {item.get('title')} - Active: {item.get('is_active', 'N/A')}")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api_items()
