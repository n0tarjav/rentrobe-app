import sys
sys.path.append('netlify/functions')
from api_simple import handler

# Test the function locally
event = {
    'path': '/api/auth/login',
    'httpMethod': 'POST',
    'body': '{"email": "demo@wearhouse.com", "password": "password123"}'
}
context = {}

result = handler(event, context)
print('Local test result:')
print(f'Status Code: {result["statusCode"]}')
print(f'Body: {result["body"]}')
