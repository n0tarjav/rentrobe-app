#!/usr/bin/env python3
"""
Test script to check the database directly for inactive items
"""

import sqlite3
import os

def test_database_items():
    """Test the database directly to see inactive items"""
    db_path = 'instance/wearhouse.db'
    if not os.path.exists(db_path):
        db_path = 'wearhouse.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all items
        cursor.execute("SELECT id, title, is_active FROM items")
        all_items = cursor.fetchall()
        
        print(f"Total items in database: {len(all_items)}")
        
        # Get active items
        cursor.execute("SELECT id, title, is_active FROM items WHERE is_active = 1")
        active_items = cursor.fetchall()
        
        print(f"Active items: {len(active_items)}")
        
        # Get inactive items
        cursor.execute("SELECT id, title, is_active FROM items WHERE is_active = 0")
        inactive_items = cursor.fetchall()
        
        print(f"Inactive items: {len(inactive_items)}")
        
        if inactive_items:
            print("\nInactive items:")
            for item in inactive_items:
                print(f"  - ID: {item[0]}, Title: {item[1]}, Active: {item[2]}")
        else:
            print("\nNo inactive items found in database")
        
        # Show first few active items
        print(f"\nFirst 5 active items:")
        for i, item in enumerate(active_items[:5]):
            print(f"  {i+1}. ID: {item[0]}, Title: {item[1]}, Active: {item[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error accessing database: {e}")

if __name__ == "__main__":
    test_database_items()
