def handler(event, context):
    """Simple test function to verify Netlify functions are working"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message": "Netlify function is working!", "event": ' + str(event) + '}'
    }