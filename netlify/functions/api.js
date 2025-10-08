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

  // Handle items endpoint
  if (event.path === '/api/items' && event.httpMethod === 'GET') {
    try {
      // Sample items data
      const sampleItems = [
        {
          id: 1,
          title: "Elegant Black Evening Gown",
          description: "Perfect for formal events and special occasions. Made with premium silk fabric.",
          price_per_day: 2500,
          size: "M",
          category: "Dresses",
          image_url: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=600&fit=crop",
          owner: {
            name: "Sarah Johnson",
            city: "Mumbai",
            rating: 4.8
          },
          is_available: true,
          date_added: "2024-01-15"
        },
        {
          id: 2,
          title: "Classic Navy Blazer",
          description: "Professional and stylish blazer for business meetings and formal events.",
          price_per_day: 1800,
          size: "L",
          category: "Blazers",
          image_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop",
          owner: {
            name: "Michael Chen",
            city: "Delhi",
            rating: 4.9
          },
          is_available: true,
          date_added: "2024-01-14"
        },
        {
          id: 3,
          title: "Vintage Denim Jacket",
          description: "Trendy vintage-style denim jacket perfect for casual outings.",
          price_per_day: 1200,
          size: "S",
          category: "Jackets",
          image_url: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=600&fit=crop",
          owner: {
            name: "Priya Sharma",
            city: "Bangalore",
            rating: 4.7
          },
          is_available: true,
          date_added: "2024-01-13"
        },
        {
          id: 4,
          title: "Designer Cocktail Dress",
          description: "Stunning cocktail dress for parties and special events. Designer label.",
          price_per_day: 3200,
          size: "M",
          category: "Dresses",
          image_url: "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop",
          owner: {
            name: "Emma Wilson",
            city: "Mumbai",
            rating: 4.9
          },
          is_available: true,
          date_added: "2024-01-12"
        },
        {
          id: 5,
          title: "Casual White Shirt",
          description: "Crisp white shirt perfect for office wear or casual meetings.",
          price_per_day: 800,
          size: "L",
          category: "Shirts",
          image_url: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=600&fit=crop",
          owner: {
            name: "David Kumar",
            city: "Chennai",
            rating: 4.6
          },
          is_available: true,
          date_added: "2024-01-11"
        },
        {
          id: 6,
          title: "Formal Trousers",
          description: "Well-fitted formal trousers for business and formal occasions.",
          price_per_day: 1000,
          size: "32",
          category: "Trousers",
          image_url: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=600&fit=crop",
          owner: {
            name: "Raj Patel",
            city: "Pune",
            rating: 4.5
          },
          is_available: true,
          date_added: "2024-01-10"
        }
      ];

      // Get query parameters
      const page = parseInt(event.queryStringParameters?.page) || 1;
      const per_page = Math.min(parseInt(event.queryStringParameters?.per_page) || 12, 100);
      const category = event.queryStringParameters?.category;
      const size = event.queryStringParameters?.size;
      const city = event.queryStringParameters?.city;
      const search = event.queryStringParameters?.search;

      // Filter items
      let filteredItems = sampleItems;

      if (category) {
        filteredItems = filteredItems.filter(item => 
          item.category.toLowerCase() === category.toLowerCase()
        );
      }

      if (size) {
        filteredItems = filteredItems.filter(item => 
          item.size.toLowerCase() === size.toLowerCase()
        );
      }

      if (city) {
        filteredItems = filteredItems.filter(item => 
          item.owner.city.toLowerCase().includes(city.toLowerCase())
        );
      }

      if (search) {
        filteredItems = filteredItems.filter(item => 
          item.title.toLowerCase().includes(search.toLowerCase()) ||
          item.description.toLowerCase().includes(search.toLowerCase())
        );
      }

      // Paginate
      const startIndex = (page - 1) * per_page;
      const endIndex = startIndex + per_page;
      const paginatedItems = filteredItems.slice(startIndex, endIndex);
      const totalPages = Math.ceil(filteredItems.length / per_page);

      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          items: paginatedItems,
          pagination: {
            page: page,
            pages: totalPages,
            per_page: per_page,
            total: filteredItems.length,
            has_next: page < totalPages,
            has_prev: page > 1
          }
        })
      };
    } catch (error) {
      return {
        statusCode: 500,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Failed to fetch items'
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
