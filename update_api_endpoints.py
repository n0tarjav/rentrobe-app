#!/usr/bin/env python3
"""
Script to update API endpoints in static files to point to your deployed backend
"""

import os
import re
from pathlib import Path

def update_api_endpoints(backend_url):
    """
    Update API endpoints in the static site to point to the deployed backend
    """
    dist_dir = Path("dist")
    
    if not dist_dir.exists():
        print("❌ Dist directory not found. Run 'python build_static.py' first.")
        return
    
    # Find all HTML files in dist directory
    html_files = list(dist_dir.glob("**/*.html"))
    
    if not html_files:
        print("❌ No HTML files found in dist directory.")
        return
    
    # API endpoint patterns to replace
    patterns = [
        (r'fetch\s*\(\s*["\']/api/', f'fetch("{backend_url}/api/'),
        (r'url:\s*["\']/api/', f'url: "{backend_url}/api/'),
        (r'["\']/api/', f'"{backend_url}/api/'),
    ]
    
    updated_files = 0
    
    for html_file in html_files:
        try:
            # Read file content
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all patterns
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            # Write back if changed
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files += 1
                print(f"✅ Updated: {html_file}")
        
        except Exception as e:
            print(f"❌ Error updating {html_file}: {e}")
    
    print(f"\n🎉 Updated {updated_files} files with backend URL: {backend_url}")

def main():
    print("🔧 API Endpoint Updater")
    print("=" * 40)
    
    # Get backend URL from user
    backend_url = input("Enter your Railway backend URL (e.g., https://your-app.up.railway.app): ").strip()
    
    if not backend_url:
        print("❌ Backend URL is required!")
        return
    
    if not backend_url.startswith('http'):
        backend_url = f"https://{backend_url}"
    
    print(f"\n🔄 Updating API endpoints to point to: {backend_url}")
    update_api_endpoints(backend_url)
    
    print("\n📝 Next steps:")
    print("1. Commit and push your changes to GitHub")
    print("2. Netlify will automatically redeploy")
    print("3. Test your deployed site!")

if __name__ == "__main__":
    main()

