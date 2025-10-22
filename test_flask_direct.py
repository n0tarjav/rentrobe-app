#!/usr/bin/env python3
"""
Test script to test the Flask app directly
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'wearhouse.db')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
os.environ['SECRET_KEY'] = 'test-secret-key'

# Import the Flask app
from app import app, db, init_db

def test_flask_direct():
    """Test the Flask app directly"""
    try:
        with app.app_context():
            # Initialize database
            init_db()
            
            # Test the items endpoint
            with app.test_client() as client:
                response = client.get('/api/items')
                
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    data = response.get_json()
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
                        
                else:
                    print(f"Error: {response.get_data(as_text=True)}")
                    
    except Exception as e:
        print(f"Error testing Flask app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_flask_direct()
