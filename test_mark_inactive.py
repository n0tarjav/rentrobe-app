#!/usr/bin/env python3
"""
Test script to mark an item as inactive and test the API
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
from app import app, db, Item

def test_mark_inactive():
    """Mark an item as inactive and test the API"""
    try:
        with app.app_context():
            # Get the first item
            item = Item.query.first()
            if item:
                print(f"Found item: {item.title} (ID: {item.id})")
                print(f"Current is_active: {item.is_active}")
                
                # Mark as inactive
                item.is_active = False
                db.session.commit()
                print(f"Marked item {item.id} as inactive")
                
                # Test the API
                with app.test_client() as client:
                    response = client.get('/api/items')
                    
                    if response.status_code == 200:
                        data = response.get_json()
                        items = data.get('items', [])
                        print(f"Number of items returned: {len(items)}")
                        
                        # Check if the inactive item is still there
                        inactive_item = next((api_item for api_item in items if api_item.get('id') == item.id), None)
                        if inactive_item:
                            print(f"ERROR: Inactive item {item.id} is still in the API response!")
                        else:
                            print(f"SUCCESS: Inactive item {item.id} is correctly filtered out!")
                            
                        # Show first few items
                        print(f"\nFirst 3 items:")
                        for i, item in enumerate(items[:3]):
                            print(f"  {i+1}. {item.get('title')} (ID: {item.get('id')}) - Active: {item.get('is_active', 'N/A')}")
                    else:
                        print(f"API Error: {response.get_data(as_text=True)}")
                        
                # Restore the item
                db_item = Item.query.get(1)  # We know it's item ID 1
                db_item.is_active = True
                db.session.commit()
                print(f"Restored item 1 as active")
            else:
                print("No items found in database")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mark_inactive()
