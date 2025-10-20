// Simple JavaScript function for Netlify
const fs = require('fs');
const path = require('path');

// File path for persistent storage
const USERS_FILE = '/tmp/users.json';

// Initialize users data
function initializeUsers() {
  try {
    if (fs.existsSync(USERS_FILE)) {
      const data = fs.readFileSync(USERS_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.log('Error reading users file:', error);
  }
  
  // Default users if file doesn't exist
  return [
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
    },
    {
      id: 2,
      name: 'Arjav',
      email: 'arjav@rentrobe.com',
      password: 'arjav0302', // In real app, this would be hashed
      phone: '+91 8319337033',
      city: 'Bhilai',
      address: 'Bhilai, Chhattisgarh',
      rating: 4.8,
      reviews_count: 15
    },
    {
      id: 3,
      name: 'Ankita',
      email: 'ankita@rentrobe.com',
      password: 'ankita1001', // In real app, this would be hashed
      phone: '+91 9876543211',
      city: 'Delhi',
      address: 'Delhi, India',
      rating: 4.9,
      reviews_count: 12
    }
  ];
}

// Save users data
function saveUsers(users) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
    return true;
  } catch (error) {
    console.log('Error saving users file:', error);
    return false;
  }
}

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
      
      console.log('Login attempt:', { email, password: password ? '***' : 'empty', path: event.path, method: event.httpMethod });
      
      // Load users from persistent storage
      const users = initializeUsers();
      
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
      console.error('Login error:', error);
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

  // Handle profile endpoint
  if ((event.path === '/api/profile' || event.path === '/.netlify/functions/api/profile') && event.httpMethod === 'GET') {
    try {
      console.log('Profile request:', { path: event.path, method: event.httpMethod });
      
      // For now, return a simple response since we're using localStorage for auth
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'Profile endpoint - use localStorage for authentication'
        })
      };
    } catch (error) {
      console.error('Profile error:', error);
      return {
        statusCode: 500,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Profile request failed'
        })
      };
    }
  }

  // Handle profile update endpoint (PUT)
  if ((event.path === '/api/profile' || event.path === '/.netlify/functions/api/profile') && event.httpMethod === 'PUT') {
    try {
      const body = JSON.parse(event.body || '{}');
      const { name, phone, city } = body;
      
      console.log('Profile update request:', { name, phone, city, path: event.path, method: event.httpMethod });
      
      // For Netlify deployment, we rely on localStorage for profile updates
      // This endpoint just returns success to acknowledge the update
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'Profile update acknowledged',
          name: name,
          phone: phone,
          city: city
        })
      };
    } catch (error) {
      console.error('Profile update error:', error);
      return {
        statusCode: 500,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Profile update failed'
        })
      };
    }
  }

  // Handle logout endpoint
  if ((event.path === '/api/auth/logout' || event.path === '/.netlify/functions/api/auth/logout') && event.httpMethod === 'POST') {
    try {
      console.log('Logout request:', { path: event.path, method: event.httpMethod });
      
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'Logout successful'
        })
      };
    } catch (error) {
      console.error('Logout error:', error);
      return {
        statusCode: 500,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Logout failed'
        })
      };
    }
  }

  // Handle items endpoint
  if (event.path === '/api/items' && event.httpMethod === 'GET') {
    try {
      // Original Sample Items Data - Complete Collection
      const sampleItems = [
        // FORMAL WEAR
        {
          id: 1,
          title: 'Black Evening Gown',
          description: 'Elegant black evening gown perfect for formal events and galas. Features intricate beadwork and a flowing silhouette.',
          category: 'formal',
          size: 'M',
          price_per_day: 800,
          deposit: 2000,
          owner: { name: 'Priya Sharma', city: 'Mumbai', rating: 4.8 },
          status: 'available',
          rating: 4.9,
          reviews: 12,
          views: 145,
          image_url: 'https://images.unsplash.com/photo-1657023855158-3878cac29205?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-15'
        },
        {
          id: 2,
          title: 'Navy Blue Business Suit',
          description: 'Professional navy suit perfect for business meetings and corporate events. Tailored fit with premium fabric.',
          category: 'formal',
          size: 'L',
          price_per_day: 700,
          deposit: 1800,
          owner: { name: 'Rajesh Kumar', city: 'Delhi', rating: 4.9 },
          status: 'available',
          rating: 4.8,
          reviews: 8,
          views: 89,
          image_url: 'https://plus.unsplash.com/premium_photo-1679440414275-f9950b562c7f?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-14'
        },
        {
          id: 3,
          title: 'White Wedding Dress',
          description: 'Stunning white wedding dress with lace details and cathedral train. Perfect for your special day.',
          category: 'formal',
          size: 'S',
          price_per_day: 1500,
          deposit: 4000,
          owner: { name: 'Kavya Nair', city: 'Kochi', rating: 4.9 },
          status: 'available',
          rating: 5.0,
          reviews: 15,
          views: 234,
          image_url: 'https://images.unsplash.com/photo-1678831165438-e2bb89db82d9?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-13'
        },
        {
          id: 4,
          title: 'Black Tuxedo',
          description: 'Classic black tuxedo for formal occasions and black-tie events. Includes bow tie and cummerbund.',
          category: 'formal',
          size: 'L',
          price_per_day: 1000,
          deposit: 2500,
          owner: { name: 'Rohit Agarwal', city: 'Delhi', rating: 4.9 },
          status: 'available',
          rating: 4.7,
          reviews: 6,
          views: 67,
          image_url: 'https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-12'
        },
        {
          id: 5,
          title: 'Grey Business Suit',
          description: 'Professional grey suit for corporate meetings and formal presentations. Modern slim fit.',
          category: 'formal',
          size: 'M',
          price_per_day: 750,
          deposit: 1900,
          owner: { name: 'Amit Sharma', city: 'Gurgaon', rating: 4.7 },
          status: 'available',
          rating: 4.6,
          reviews: 9,
          views: 78,
          image_url: 'https://plus.unsplash.com/premium_photo-1682430740985-acbce7ec295e?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-11'
        },
        {
          id: 6,
          title: 'Maroon Blazer',
          description: 'Elegant maroon blazer for formal occasions and business casual events.',
          category: 'formal',
          size: 'S',
          price_per_day: 650,
          deposit: 1600,
          owner: { name: 'Priyanka Das', city: 'Kolkata', rating: 4.7 },
          status: 'available',
          rating: 4.5,
          reviews: 7,
          views: 56,
          image_url: 'https://plus.unsplash.com/premium_photo-1730828573906-f44ac401de96?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-10'
        },

        // PARTY OUTFITS
        {
          id: 7,
          title: 'Premium Cocktail Dress',
          description: 'Beautiful red cocktail dress from premium brand. Perfect for cocktail parties and evening events.',
          category: 'party',
          size: 'S',
          price_per_day: 600,
          deposit: 1500,
          owner: { name: 'Anjali Reddy', city: 'Bangalore', rating: 4.6 },
          status: 'available',
          rating: 4.8,
          reviews: 11,
          views: 123,
          image_url: 'https://images.unsplash.com/photo-1721182421063-19a6c711b719?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-09'
        },
        {
          id: 8,
          title: 'Pink Party Dress',
          description: 'Vibrant pink dress perfect for parties and celebrations. Features sequin details and flowing fabric.',
          category: 'party',
          size: 'M',
          price_per_day: 450,
          deposit: 1000,
          owner: { name: 'Riya Jain', city: 'Jaipur', rating: 4.6 },
          status: 'available',
          rating: 4.7,
          reviews: 8,
          views: 92,
          image_url: 'https://images.unsplash.com/photo-1708121691161-b8b11bebc761?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-08'
        },
        {
          id: 9,
          title: 'Green Cocktail Dress',
          description: 'Elegant green cocktail dress for special events and dinner parties.',
          category: 'party',
          size: 'S',
          price_per_day: 550,
          deposit: 1300,
          owner: { name: 'Pooja Kapoor', city: 'Chandigarh', rating: 4.6 },
          status: 'available',
          rating: 4.6,
          reviews: 5,
          views: 73,
          image_url: 'https://images.unsplash.com/photo-1566479179817-c0c8e5c7b7b8?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-07'
        },
        {
          id: 10,
          title: 'Purple Party Gown',
          description: 'Stunning purple gown perfect for evening parties and special celebrations.',
          category: 'party',
          size: 'L',
          price_per_day: 700,
          deposit: 1700,
          owner: { name: 'Shreya Patel', city: 'Surat', rating: 4.5 },
          status: 'available',
          rating: 4.9,
          reviews: 13,
          views: 156,
          image_url: 'https://images.unsplash.com/photo-1566479179817-c0c8e5c7b7b8?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-06'
        },
        {
          id: 11,
          title: 'Silver Sequin Dress',
          description: 'Glamorous silver sequin dress for parties and New Year celebrations.',
          category: 'party',
          size: 'M',
          price_per_day: 800,
          deposit: 2000,
          owner: { name: 'Natasha Malhotra', city: 'Delhi', rating: 4.6 },
          status: 'available',
          rating: 4.8,
          reviews: 10,
          views: 134,
          image_url: 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-05'
        },
        {
          id: 12,
          title: 'Blue Velvet Dress',
          description: 'Luxurious blue velvet dress perfect for winter parties and elegant events.',
          category: 'party',
          size: 'M',
          price_per_day: 650,
          deposit: 1600,
          owner: { name: 'Ishita Agarwal', city: 'Delhi', rating: 4.9 },
          status: 'available',
          rating: 4.7,
          reviews: 9,
          views: 87,
          image_url: 'https://images.unsplash.com/photo-1566479179817-c0c8e5c7b7b8?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-04'
        },

        // TRADITIONAL WEAR
        {
          id: 13,
          title: 'Traditional Lehenga',
          description: 'Beautiful traditional lehenga with intricate embroidery work. Perfect for weddings and festivals.',
          category: 'traditional',
          size: 'M',
          price_per_day: 1200,
          deposit: 3000,
          owner: { name: 'Meera Patel', city: 'Ahmedabad', rating: 4.7 },
          status: 'available',
          rating: 4.9,
          reviews: 14,
          views: 189,
          image_url: 'https://plus.unsplash.com/premium_photo-1682096032284-0b2ab20b65dd?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-03'
        },
        {
          id: 14,
          title: 'Golden Saree',
          description: 'Traditional golden saree with intricate work. Perfect for weddings and special occasions.',
          category: 'traditional',
          size: 'One Size',
          price_per_day: 900,
          deposit: 2200,
          owner: { name: 'Lakshmi Iyer', city: 'Chennai', rating: 4.8 },
          status: 'available',
          rating: 4.8,
          reviews: 11,
          views: 145,
          image_url: 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-02'
        },
        {
          id: 15,
          title: 'Red Traditional Kurta',
          description: 'Beautiful red kurta with traditional embroidery. Perfect for festivals and cultural events.',
          category: 'traditional',
          size: 'L',
          price_per_day: 400,
          deposit: 900,
          owner: { name: 'Sanjay Gupta', city: 'Varanasi', rating: 4.4 },
          status: 'available',
          rating: 4.5,
          reviews: 6,
          views: 67,
          image_url: 'https://images.unsplash.com/photo-1622470953794-aa9c70b0fb9d?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2024-01-01'
        },
        {
          id: 16,
          title: 'Silk Dupatta',
          description: 'Beautiful silk dupatta with golden border. Perfect complement to traditional outfits.',
          category: 'traditional',
          size: 'One Size',
          price_per_day: 300,
          deposit: 700,
          owner: { name: 'Anita Joshi', city: 'Jodhpur', rating: 4.8 },
          status: 'available',
          rating: 4.6,
          reviews: 8,
          views: 54,
          image_url: 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-31'
        },
        {
          id: 17,
          title: 'Banarasi Silk Saree',
          description: 'Exquisite Banarasi silk saree with gold work. A masterpiece of traditional craftsmanship.',
          category: 'traditional',
          size: 'One Size',
          price_per_day: 1100,
          deposit: 2800,
          owner: { name: 'Geeta Sharma', city: 'Varanasi', rating: 4.8 },
          status: 'available',
          rating: 5.0,
          reviews: 16,
          views: 201,
          image_url: 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-30'
        },
        {
          id: 18,
          title: 'Punjabi Suit Set',
          description: 'Complete Punjabi suit set with dupatta. Perfect for cultural celebrations and festivals.',
          category: 'traditional',
          size: 'M',
          price_per_day: 500,
          deposit: 1200,
          owner: { name: 'Simran Kaur', city: 'Chandigarh', rating: 4.7 },
          status: 'available',
          rating: 4.7,
          reviews: 9,
          views: 98,
          image_url: 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-29'
        },

        // CASUAL WEAR
        {
          id: 19,
          title: 'Casual Denim Jacket',
          description: 'Trendy denim jacket perfect for casual outings and weekend wear.',
          category: 'casual',
          size: 'L',
          price_per_day: 300,
          deposit: 800,
          owner: { name: 'Rahul Singh', city: 'Pune', rating: 4.5 },
          status: 'available',
          rating: 4.4,
          reviews: 7,
          views: 76,
          image_url: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-28'
        },
        {
          id: 20,
          title: 'Blue Casual Shirt',
          description: 'Comfortable blue casual shirt for everyday wear and casual meetings.',
          category: 'casual',
          size: 'M',
          price_per_day: 200,
          deposit: 500,
          owner: { name: 'Arjun Mehta', city: 'Hyderabad', rating: 4.7 },
          status: 'available',
          rating: 4.3,
          reviews: 5,
          views: 45,
          image_url: 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-27'
        },
        {
          id: 21,
          title: 'White Sneakers',
          description: 'Trendy white sneakers perfect for casual outfits and daily wear.',
          category: 'casual',
          size: '8',
          price_per_day: 250,
          deposit: 600,
          owner: { name: 'Neha Verma', city: 'Lucknow', rating: 4.7 },
          status: 'available',
          rating: 4.5,
          reviews: 8,
          views: 67,
          image_url: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-26'
        },
        {
          id: 22,
          title: 'Denim Jeans',
          description: 'Classic blue denim jeans for casual wear. Comfortable fit and durable fabric.',
          category: 'casual',
          size: '32',
          price_per_day: 180,
          deposit: 450,
          owner: { name: 'Karan Singh', city: 'Amritsar', rating: 4.6 },
          status: 'available',
          rating: 4.2,
          reviews: 6,
          views: 43,
          image_url: 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-25'
        },
        {
          id: 23,
          title: 'Cotton T-Shirt',
          description: 'Comfortable cotton t-shirt for daily wear. Soft fabric and perfect fit.',
          category: 'casual',
          size: 'L',
          price_per_day: 150,
          deposit: 350,
          owner: { name: 'Suresh Kumar', city: 'Patna', rating: 4.5 },
          status: 'available',
          rating: 4.1,
          reviews: 4,
          views: 32,
          image_url: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-24'
        },
        {
          id: 24,
          title: 'Casual Summer Dress',
          description: 'Light and breezy summer dress perfect for casual outings and beach trips.',
          category: 'casual',
          size: 'S',
          price_per_day: 280,
          deposit: 650,
          owner: { name: 'Tanvi Joshi', city: 'Bangalore', rating: 4.8 },
          status: 'available',
          rating: 4.6,
          reviews: 9,
          views: 89,
          image_url: 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-23'
        },

        // ACCESSORIES
        {
          id: 25,
          title: 'Luxury Handbag',
          description: 'Luxury handbag in pristine condition. Perfect for formal and casual occasions.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 500,
          deposit: 1200,
          owner: { name: 'Sneha Gupta', city: 'Chennai', rating: 4.8 },
          status: 'available',
          rating: 4.7,
          reviews: 12,
          views: 134,
          image_url: 'https://images.unsplash.com/photo-1652427019217-3ded1a356f10?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-22'
        },
        {
          id: 26,
          title: 'Luxury Watch',
          description: 'Luxury watch in excellent condition. Perfect accessory for formal occasions.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 800,
          deposit: 2000,
          owner: { name: 'Vikram Shah', city: 'Mumbai', rating: 4.5 },
          status: 'available',
          rating: 4.8,
          reviews: 10,
          views: 123,
          image_url: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-21'
        },
        {
          id: 27,
          title: 'Pearl Necklace',
          description: 'Elegant pearl necklace for special occasions and formal events.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 600,
          deposit: 1500,
          owner: { name: 'Divya Rao', city: 'Bangalore', rating: 4.8 },
          status: 'available',
          rating: 4.9,
          reviews: 14,
          views: 167,
          image_url: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-20'
        },
        {
          id: 28,
          title: 'Premium Sunglasses',
          description: 'Stylish sunglasses with UV protection. Perfect for outdoor events and travel.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 350,
          deposit: 800,
          owner: { name: 'Rahul Khanna', city: 'Mumbai', rating: 4.9 },
          status: 'available',
          rating: 4.5,
          reviews: 7,
          views: 78,
          image_url: 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-19'
        },
        {
          id: 29,
          title: 'Designer Clutch',
          description: 'Elegant designer clutch perfect for evening parties and formal events.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 400,
          deposit: 950,
          owner: { name: 'Ritu Singh', city: 'Lucknow', rating: 4.8 },
          status: 'available',
          rating: 4.6,
          reviews: 8,
          views: 92,
          image_url: 'https://images.unsplash.com/photo-1652427019217-3ded1a356f10?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-18'
        },
        {
          id: 30,
          title: 'Statement Earrings',
          description: 'Bold statement earrings perfect for parties and special occasions.',
          category: 'accessories',
          size: 'One Size',
          price_per_day: 250,
          deposit: 600,
          owner: { name: 'Deepika Nair', city: 'Kochi', rating: 4.7 },
          status: 'available',
          rating: 4.4,
          reviews: 6,
          views: 54,
          image_url: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-17'
        },

        // DESIGNER ITEMS
        {
          id: 31,
          title: 'Gucci Evening Dress',
          description: 'Authentic Gucci evening dress in pristine condition. A true luxury piece.',
          category: 'designer',
          size: 'M',
          price_per_day: 2000,
          deposit: 5000,
          owner: { name: 'Aditya Kapoor', city: 'Mumbai', rating: 4.7 },
          status: 'available',
          rating: 5.0,
          reviews: 18,
          views: 289,
          image_url: 'https://images.unsplash.com/photo-1657023855158-3878cac29205?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-16'
        },
        {
          id: 32,
          title: 'Versace Blazer',
          description: 'Designer Versace blazer for the fashion-forward individual. Premium quality.',
          category: 'designer',
          size: 'L',
          price_per_day: 1800,
          deposit: 4500,
          owner: { name: 'Rohan Desai', city: 'Pune', rating: 4.6 },
          status: 'available',
          rating: 4.9,
          reviews: 15,
          views: 234,
          image_url: 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-15'
        },
        {
          id: 33,
          title: 'Prada Handbag',
          description: 'Authentic Prada handbag in excellent condition. A timeless luxury accessory.',
          category: 'designer',
          size: 'One Size',
          price_per_day: 1500,
          deposit: 3800,
          owner: { name: 'Nikhil Rao', city: 'Hyderabad', rating: 4.5 },
          status: 'available',
          rating: 4.8,
          reviews: 12,
          views: 178,
          image_url: 'https://images.unsplash.com/photo-1652427019217-3ded1a356f10?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-14'
        },
        {
          id: 34,
          title: 'Armani Suit',
          description: 'Giorgio Armani suit in navy blue. Perfect for high-profile business meetings.',
          category: 'designer',
          size: 'M',
          price_per_day: 2200,
          deposit: 5500,
          owner: { name: 'Varun Malhotra', city: 'Delhi', rating: 4.6 },
          status: 'available',
          rating: 4.9,
          reviews: 16,
          views: 267,
          image_url: 'https://plus.unsplash.com/premium_photo-1679440414275-f9950b562c7f?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-13'
        },
        {
          id: 35,
          title: 'Chanel Dress',
          description: 'Classic Chanel dress in black. An iconic piece from the luxury fashion house.',
          category: 'designer',
          size: 'S',
          price_per_day: 2500,
          deposit: 6000,
          owner: { name: 'Akash Patel', city: 'Ahmedabad', rating: 4.9 },
          status: 'available',
          rating: 5.0,
          reviews: 20,
          views: 345,
          image_url: 'https://images.unsplash.com/photo-1657023855158-3878cac29205?w=400&h=600&fit=crop&crop=center',
          is_available: true,
          date_added: '2023-12-12'
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
      
      // Load users from persistent storage
      const users = initializeUsers();
      
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
      
      // Save users to persistent storage
      const saved = saveUsers(users);
      if (!saved) {
        console.log('Warning: Could not save user data to file');
      }
      
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
