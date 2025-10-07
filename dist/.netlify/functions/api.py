import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set up database path for Netlify
# Database will be in the same directory as the function
db_path = os.path.join(os.path.dirname(__file__), 'wearhouse.db')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

# Import Flask app
from app import app, db, init_db

def handler(event, context):
    """
    Netlify serverless function handler for Flask API
    """
    try:
        # Parse the event
        path = event.get('path', '')
        http_method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        body = event.get('body', '')
        query_string = event.get('queryStringParameters', {}) or {}
        
        # Remove /api prefix from path for Flask routing
        if path.startswith('/api'):
            path = path[4:]  # Remove '/api' prefix
        if not path:
            path = '/'
        
        # Handle CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
                'body': ''
            }
        
        # Initialize database if needed
        with app.app_context():
            try:
                init_db()
                print(f"Database initialized successfully")
            except Exception as db_error:
                print(f"Database init error: {str(db_error)}")
                # Continue anyway for testing
        
        # Create a mock request context
        print(f"Handling request: {http_method} {path}")
        print(f"Body: {body}")
        
        with app.test_request_context(
            path=path,
            method=http_method,
            headers=headers,
            data=body,
            query_string=query_string
        ):
            # Handle the request
            response = app.full_dispatch_request()
            print(f"Response status: {response.status_code}")
            
            # Extract response data
            response_data = response.get_data(as_text=True)
            status_code = response.status_code
            response_headers = dict(response.headers)
            
            # Handle JSON responses
            if response_headers.get('Content-Type', '').startswith('application/json'):
                try:
                    response_data = json.loads(response_data)
                except json.JSONDecodeError:
                    pass
            
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
                'body': json.dumps(response_data)
            }
    
    except Exception as e:
        print(f"Error in API handler: {str(e)}")
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
