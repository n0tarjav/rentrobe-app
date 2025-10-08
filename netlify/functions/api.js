// Simple JavaScript function for Netlify
exports.handler = async (event, context) => {
  // Handle CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Simple test endpoint
  if (event.path === '/api/test' || event.path === '/.netlify/functions/api/test') {
    return {
      statusCode: 200,
      headers: {
        ...headers,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: 'Test function working!',
        status: 'success',
        path: event.path,
        method: event.httpMethod
      })
    };
  }

  // Handle login endpoint - check both possible paths
  if ((event.path === '/api/auth/login' || event.path === '/.netlify/functions/api/auth/login') && event.httpMethod === 'POST') {
    try {
      const body = JSON.parse(event.body || '{}');
      const { email, password } = body;
      
      console.log('Login attempt:', { email, password, path: event.path, method: event.httpMethod });
      
      // Simple demo login check
      if (email === 'demo@wearhouse.com' && password === 'password123') {
        const user = {
          id: 1,
          name: 'Demo User',
          email: 'demo@wearhouse.com',
          phone: '+91 9876543210',
          city: 'Mumbai',
          address: '123 Fashion Street, Mumbai',
          rating: 5.0,
          reviews_count: 10
        };
        
        return {
          statusCode: 200,
          headers: {
            ...headers,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: 'Login successful',
            user: user
          })
        };
      } else {
        return {
          statusCode: 401,
          headers: {
            ...headers,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            error: 'Invalid email or password'
          })
        };
      }
    } catch (error) {
      return {
        statusCode: 400,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Invalid request data'
        })
      };
    }
  }

  // Default response
  return {
    statusCode: 200,
    headers: {
      ...headers,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: 'API function working!',
      status: 'success',
      path: event.path,
      method: event.httpMethod
    })
  };
};
