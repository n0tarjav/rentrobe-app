// Simple JavaScript function for Netlify
// Simple in-memory storage for demo purposes
let users = [
  {
    id: 1,
    name: 'Demo User',
    email: 'demo@wearhouse.com',
    password: 'password123', // In real app, this would be hashed
    phone: '+91 9876543210',
    city: 'Mumbai',
    address: '123 Fashion Street, Mumbai',
    rating: 5.0,
    reviews_count: 10
  }
];

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
      
      // Find user in our users array
      const user = users.find(u => u.email === email && u.password === password);
      
      if (user) {
        // Return user without password
        const { password: _, ...userWithoutPassword } = user;
        
        return {
          statusCode: 200,
          headers: {
            ...headers,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: 'Login successful',
            user: userWithoutPassword
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

  // Handle signup endpoint
  if (event.path === '/api/auth/register' && event.httpMethod === 'POST') {
    try {
      const body = JSON.parse(event.body || '{}');
      const { name, email, password, phone, city } = body;
      
      console.log('Signup attempt:', { name, email, phone, city });
      
      // Validate required fields
      if (!name || !email || !password || !phone || !city) {
        return {
          statusCode: 400,
          headers: {
            ...headers,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            error: 'All fields are required'
          })
        };
      }
      
      // Check if email already exists
      const existingUser = users.find(u => u.email === email);
      if (existingUser) {
        return {
          statusCode: 400,
          headers: {
            ...headers,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            error: 'Email already registered'
          })
        };
      }
      
      // Create new user
      const user = {
        id: Date.now(), // Simple ID generation
        name: name,
        email: email,
        password: password, // In real app, this would be hashed
        phone: phone,
        city: city,
        address: '',
        rating: 0.0,
        reviews_count: 0
      };
      
      // Add user to our users array
      users.push(user);
      
      // Return user without password
      const { password: _, ...userWithoutPassword } = user;
      
      return {
        statusCode: 201,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'Registration successful',
          user: userWithoutPassword
        })
      };
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
