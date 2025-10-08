#!/usr/bin/env python3
import sqlite3
import os

# Check if database exists
db_path = 'instance/wearhouse.db'
if os.path.exists(db_path):
    print(f"Database exists at: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    # Check users table
    if ('users',) in tables:
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"User count: {user_count}")
        
        cursor.execute("SELECT email, name FROM users LIMIT 5;")
        sample_users = cursor.fetchall()
        print(f"Sample users: {sample_users}")
    else:
        print("Users table does not exist!")
    
    conn.close()
else:
    print(f"Database does not exist at: {db_path}")
    
    # Check if instance directory exists
    if os.path.exists('instance'):
        print("Instance directory exists")
        print("Contents:", os.listdir('instance'))
    else:
        print("Instance directory does not exist")
