"""
Netlify serverless function for API endpoints
This handles the backend API for your static site
"""

import json
import os
from http.server import BaseHTTPRequestHandler
import urllib.parse

# This would need to be adapted to work with your database
# For now, this is a template showing how to structure it

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        
        # Route to appropriate handler
        if path_parts[1] == 'api':
            if path_parts[2] == 'categories':
                self.handle_categories()
            elif path_parts[2] == 'items':
                self.handle_items()
            else:
                self.send_error(404)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        
        if path_parts[1] == 'api':
            if path_parts[2] == 'auth':
                if path_parts[3] == 'login':
                    self.handle_login()
                elif path_parts[3] == 'register':
                    self.handle_register()
                else:
                    self.send_error(404)
            else:
                self.send_error(404)
        else:
            self.send_error(404)
    
    def handle_categories(self):
        """Return categories data"""
        # This would typically fetch from a database
        # For now, return static data
        categories = [
            {"id": 1, "name": "Formal Wear", "slug": "formal", "icon": "👔"},
            {"id": 2, "name": "Casual Wear", "slug": "casual", "icon": "👕"},
            {"id": 3, "name": "Party Outfits", "slug": "party", "icon": "✨"},
            {"id": 4, "name": "Traditional", "slug": "traditional", "icon": "🥻"},
            {"id": 5, "name": "Accessories", "slug": "accessories", "icon": "👜"},
            {"id": 6, "name": "Designer", "slug": "designer", "icon": "💎"}
        ]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(categories).encode())
    
    def handle_items(self):
        """Return items data"""
        # This would typically fetch from a database
        items = [
            {
                "id": 1,
                "title": "Elegant Black Evening Gown",
                "description": "Stunning black evening gown perfect for formal events.",
                "category": "Formal Wear",
                "size": "M",
                "price": 800,
                "deposit": 2000,
                "status": "available",
                "condition": "excellent",
                "rating": 4.5,
                "reviews": 12,
                "views": 45,
                "images": ["sample1.jpg"],
                "owner": {
                    "id": 1,
                    "name": "Demo User",
                    "city": "Mumbai",
                    "initial": "D",
                    "rating": 4.8,
                    "reviews_count": 25
                }
            }
        ]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"items": items, "pagination": {"page": 1, "pages": 1, "per_page": 12, "total": 1, "has_next": False, "has_prev": False}}).encode())
    
    def handle_login(self):
        """Handle user login"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # This would typically validate against a database
        # For demo purposes, accept any email/password
        if data.get('email') and data.get('password'):
            response = {
                "message": "Login successful",
                "user": {
                    "id": 1,
                    "name": "Demo User",
                    "email": data['email'],
                    "city": "Mumbai",
                    "rating": 4.8,
                    "reviews_count": 25
                }
            }
            self.send_response(200)
        else:
            response = {"error": "Email and password are required"}
            self.send_response(400)
        
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_register(self):
        """Handle user registration"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # This would typically save to a database
        response = {
            "message": "Registration successful",
            "user": {
                "id": 1,
                "name": data.get('name', 'New User'),
                "email": data.get('email'),
                "city": data.get('city', 'Unknown'),
                "rating": 0,
                "reviews_count": 0
            }
        }
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
