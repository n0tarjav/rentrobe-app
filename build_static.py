#!/usr/bin/env python3
"""
Build script to generate static site from Flask app
This creates a static version of your site for Netlify deployment
"""

import os
import shutil
import json
from pathlib import Path
from flask import Flask, render_template
from app import app, db, init_db, create_sample_data

def build_static_site():
    """Build static version of the site"""
    
    # Create output directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy static files
    static_dir = Path("static")
    if static_dir.exists():
        shutil.copytree(static_dir, dist_dir / "static")
    
    # Initialize database and create sample data
    with app.app_context():
        init_db()
        create_sample_data()
        
        # Get all data needed for static generation
        from app import Category, Item, User
        
        categories = Category.query.filter_by(is_active=True).all()
        items = Item.query.filter_by(is_active=True).all()
        users = User.query.all()
        
        # Create data files
        data_dir = dist_dir / "data"
        data_dir.mkdir()
        
        # Save categories
        with open(data_dir / "categories.json", "w") as f:
            json.dump([cat.to_dict() for cat in categories], f, indent=2)
        
        # Save items
        with open(data_dir / "items.json", "w") as f:
            json.dump([item.to_dict() for item in items], f, indent=2)
        
        # Save users (without sensitive data)
        users_data = []
        for user in users:
            user_dict = user.to_dict()
            # Remove sensitive fields
            user_dict.pop('email', None)
            user_dict.pop('phone', None)
            user_dict.pop('address', None)
            users_data.append(user_dict)
        
        with open(data_dir / "users.json", "w") as f:
            json.dump(users_data, f, indent=2)
    
    # Generate static HTML
    with app.app_context():
        # Render main page
        html_content = render_template('index.html')
        
        # Write to dist/index.html
        with open(dist_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    print("Static site built successfully!")
    print(f"Output directory: {dist_dir.absolute()}")
    print("You can now deploy the 'dist' folder to Netlify")

if __name__ == "__main__":
    build_static_site()
