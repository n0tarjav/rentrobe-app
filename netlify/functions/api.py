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

# Set secret key for Netlify
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'wearhouse-netlify-secret-key-change-in-production')

# Set session configuration for Netlify
os.environ['SESSION_COOKIE_SECURE'] = 'True'  # Use HTTPS for production
os.environ['SESSION_COOKIE_HTTPONLY'] = 'True'
os.environ['SESSION_COOKIE_SAMESITE'] = 'Lax'
os.environ['SESSION_COOKIE_DOMAIN'] = '.netlify.app'  # Allow subdomain cookies

# Import Flask app
from app import app, db, init_db

def handler(event, context):
    """
    Netlify serverless function handler for Flask API
    """
    print(f"Function called with event: {event}")
    print(f"Context: {context}")
    
    try:
        # Parse the event
        path = event.get('path', '')
        http_method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        body = event.get('body', '')
        query_string = event.get('queryStringParameters', {}) or {}
        
        # Convert headers to lowercase for Flask compatibility
        headers = {k.lower(): v for k, v in headers.items()}
        
        # Remove /api prefix from path for Flask routing
        if path.startswith('/api'):
            path = path[4:]  # Remove '/api' prefix
        if not path:
            path = '/'
        
        # Handle query string parameters
        if query_string:
            query_string = '&'.join([f"{k}={v}" for k, v in query_string.items()])
        else:
            query_string = ''
        
        # Handle CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Cookie, Set-Cookie',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Credentials': 'true'
                },
                'body': ''
            }
        
        # Initialize database if needed
        with app.app_context():
            try:
                # Always try to initialize database to ensure demo user exists
                print(f"Initializing database at {db_path}")
                init_db()
                print(f"Database initialized successfully")
                
                # Check if demo user exists, create if not
                from app import User, bcrypt
                demo_user = User.query.filter_by(email='demo@wearhouse.com').first()
                if not demo_user:
                    print("Creating demo user...")
                    demo_user = User(
                        name='Demo User',
                        email='demo@wearhouse.com',
                        password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                        phone='+91 9876543210',
                        city='Mumbai',
                        address='123 Fashion Street, Mumbai',
                        is_verified=True
                    )
                    db.session.add(demo_user)
                    db.session.commit()
                    print("Demo user created successfully")
                else:
                    print("Demo user already exists")
                    
            except Exception as db_error:
                print(f"Database init error: {str(db_error)}")
                import traceback
                traceback.print_exc()
                # Continue anyway for testing
        
        # Create a mock request context
        print(f"Handling request: {http_method} {path}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Query string: {query_string}")
        
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
            
            # Prepare response headers
            netlify_headers = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, Cookie, Set-Cookie',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Credentials': 'true'
            }
            
            # Pass through any Set-Cookie headers from Flask
            if 'Set-Cookie' in response_headers:
                netlify_headers['Set-Cookie'] = response_headers['Set-Cookie']
            
            return {
                'statusCode': status_code,
                'headers': netlify_headers,
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
