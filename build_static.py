#!/usr/bin/env python3
"""
Build script for Netlify deployment
Creates static files and prepares the site for deployment
"""

import os
import shutil
import sys
from pathlib import Path

def build_static_site():
    """Build static site for Netlify deployment"""
    
    # Create dist directory
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    print("Building static site...")
    
    # Copy static files
    static_src = Path('static')
    static_dst = dist_dir / 'static'
    if static_src.exists():
        shutil.copytree(static_src, static_dst)
        print(f"[OK] Copied static files to {static_dst}")
    
    # Copy templates
    templates_src = Path('templates')
    templates_dst = dist_dir / 'templates'
    if templates_src.exists():
        shutil.copytree(templates_src, templates_dst)
        print(f"[OK] Copied templates to {templates_dst}")
    
    # Copy main HTML file as index.html
    index_src = templates_dst / 'index.html'
    index_dst = dist_dir / 'index.html'
    if index_src.exists():
        shutil.copy2(index_src, index_dst)
        print(f"[OK] Created index.html")
    
    # Copy database file
    db_src = Path('instance/wearhouse.db')
    db_dst = dist_dir / 'wearhouse.db'
    if db_src.exists():
        shutil.copy2(db_src, db_dst)
        print(f"[OK] Copied database to {db_dst}")
    else:
        print("[WARNING] Database file not found at instance/wearhouse.db")
    
    # Create netlify directory structure
    netlify_dir = dist_dir / '.netlify'
    netlify_dir.mkdir()
    
    functions_dir = netlify_dir / 'functions'
    functions_dir.mkdir()
    
    # Copy API function
    api_src = Path('netlify/functions/api.py')
    api_dst = functions_dir / 'api.py'
    if api_src.exists():
        shutil.copy2(api_src, api_dst)
        print(f"[OK] Copied API function to {api_dst}")
    
    # Copy database to functions directory
    db_src = Path('instance/wearhouse.db')
    db_dst = functions_dir / 'wearhouse.db'
    if db_src.exists():
        shutil.copy2(db_src, db_dst)
        print(f"[OK] Copied database to functions directory")
    
    # Copy requirements.txt
    req_src = Path('requirements.txt')
    req_dst = dist_dir / 'requirements.txt'
    if req_src.exists():
        shutil.copy2(req_src, req_dst)
        print(f"[OK] Copied requirements.txt")
    
    # Copy app.py
    app_src = Path('app.py')
    app_dst = dist_dir / 'app.py'
    if app_src.exists():
        shutil.copy2(app_src, app_dst)
        print(f"[OK] Copied app.py")
    
    # Create a simple _redirects file for SPA routing
    redirects_file = dist_dir / '_redirects'
    with open(redirects_file, 'w') as f:
        f.write("""# API routes
/api/* /.netlify/functions/api 200!

# SPA routes - redirect everything else to index.html
/* /index.html 200
""")
    print(f"[OK] Created _redirects file")
    
    # Create a simple _headers file for caching
    headers_file = dist_dir / '_headers'
    with open(headers_file, 'w') as f:
        f.write("""# Static assets caching
/static/*
  Cache-Control: public, max-age=31536000

# API responses
/api/*
  Cache-Control: no-cache

# HTML files
/*.html
  Cache-Control: no-cache
""")
    print(f"[OK] Created _headers file")
    
    print("\n[SUCCESS] Static site build completed!")
    print(f"[INFO] Output directory: {dist_dir.absolute()}")
    print("\n[READY] Ready for Netlify deployment!")

if __name__ == '__main__':
    build_static_site()
