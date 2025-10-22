#!/usr/bin/env python3
"""
Script to check and remove accessories items from the database
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
from app import app, db, Item, Category

def check_and_remove_accessories():
    """Check for accessories items and remove them"""
    try:
        with app.app_context():
            # First, check if there's an accessories category
            accessories_category = Category.query.filter_by(slug='accessories').first()
            
            if accessories_category:
                print(f"Found accessories category: {accessories_category.name} (ID: {accessories_category.id})")
                
                # Find all items in accessories category
                accessories_items = Item.query.filter_by(category_id=accessories_category.id).all()
                print(f"Found {len(accessories_items)} accessories items:")
                
                for item in accessories_items:
                    print(f"  - {item.title} (ID: {item.id}) - Active: {item.is_active}")
                
                if accessories_items:
                    # Mark all accessories items as inactive
                    for item in accessories_items:
                        item.is_active = False
                    
                    db.session.commit()
                    print(f"\nMarked {len(accessories_items)} accessories items as inactive")
                else:
                    print("No accessories items found")
            else:
                print("No accessories category found")
                
            # Also check for items with category 'accessories' in the title or description
            accessories_items_by_name = Item.query.filter(
                db.or_(
                    Item.title.ilike('%accessories%'),
                    Item.title.ilike('%accessory%'),
                    Item.description.ilike('%accessories%'),
                    Item.description.ilike('%accessory%')
                )
            ).all()
            
            if accessories_items_by_name:
                print(f"\nFound {len(accessories_items_by_name)} items with 'accessories' in name/description:")
                for item in accessories_items_by_name:
                    print(f"  - {item.title} (ID: {item.id}) - Active: {item.is_active}")
                
                # Mark these as inactive too
                for item in accessories_items_by_name:
                    item.is_active = False
                
                db.session.commit()
                print(f"Marked {len(accessories_items_by_name)} additional items as inactive")
            
            # Check final count of active items
            active_items = Item.query.filter_by(is_active=True).all()
            print(f"\nTotal active items remaining: {len(active_items)}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_remove_accessories()
