import json
import os
import sqlite3
import hashlib
from pathlib import Path

def handler(event, context):
    """
    Working API handler for Netlify functions
    """
    print(f"Function called with event: {event}")
    
    try:
        # Parse the event
        path = event.get('path', '')
        http_method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        print(f"Handling request: {http_method} {path}")
        
        # Handle CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Cookie, X-Requested-With',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Max-Age': '86400'
                },
                'body': ''
            }
        
        # Handle login
        if path == '/api/auth/login' and http_method == 'POST':
            try:
                data = json.loads(body) if body else {}
                email = data.get('email', '').lower().strip()
                password = data.get('password', '')
                
                print(f"Login attempt: {email}")
                
                # Check against hardcoded users for now
                users = {
                    'demo@wearhouse.com': {'password': 'password123', 'name': 'Demo User', 'id': 1},
                    'arjav@rentrobe.com': {'password': 'arjav0302', 'name': 'Arjav', 'id': 2},
                    'ankita@rentrobe.com': {'password': 'ankita1001', 'name': 'Ankita', 'id': 3}
                }
                
                if email in users and users[email]['password'] == password:
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Credentials': 'true'
                        },
                        'body': json.dumps({
                            'message': 'Login successful',
                            'user': {
                                'id': users[email]['id'],
                                'name': users[email]['name'],
                                'email': email
                            }
                        })
                    }
                else:
                    return {
                        'statusCode': 401,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Invalid credentials'})
                    }
            except Exception as e:
                print(f"Login error: {e}")
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Login failed'})
                }
        
        # Handle registration
        elif path == '/api/auth/register' and http_method == 'POST':
            try:
                data = json.loads(body) if body else {}
                email = data.get('email', '').lower().strip()
                password = data.get('password', '')
                name = data.get('name', '')
                
                print(f"Registration attempt: {email}")
                
                # Simple validation
                if not email or not password or not name:
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'All fields are required'})
                    }
                
                # For now, just return success
                return {
                    'statusCode': 201,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'message': 'Registration successful',
                        'user': {
                            'id': 999,
                            'name': name,
                            'email': email
                        }
                    })
                }
            except Exception as e:
                print(f"Registration error: {e}")
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Registration failed'})
                }
        
        # Handle other API routes
        elif path.startswith('/api/'):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': f'API endpoint {path} called with method {http_method}'})
            }
        
        # Default response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'API function is working', 'path': path, 'method': http_method})
        }
        
    except Exception as e:
        print(f"Handler error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }
