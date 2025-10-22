import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set up database path for Netlify
db_path = os.path.join(os.path.dirname(__file__), 'wearhouse.db')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
os.environ['SECRET_KEY'] = 'wearhouse-netlify-secret-key-change-in-production'

def handler(event, context):
    """Simplified API handler for debugging"""
    print(f"Event: {event}")
    print(f"Context: {context}")
    
    try:
        path = event.get('path', '')
        http_method = event.get('httpMethod', 'GET')
        body = event.get('body', '')
        
        print(f"Path: {path}, Method: {http_method}")
        
        # Handle login specifically
        if path == '/api/auth/login' and http_method == 'POST':
            try:
                data = json.loads(body) if body else {}
                email = data.get('email', '')
                password = data.get('password', '')
                
                print(f"Login attempt: {email}")
                
                # Simple hardcoded check for demo user
                if email == 'demo@wearhouse.com' and password == 'password123':
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
                                'id': 1,
                                'name': 'Demo User',
                                'email': 'demo@wearhouse.com'
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
