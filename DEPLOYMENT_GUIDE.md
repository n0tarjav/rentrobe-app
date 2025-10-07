# Netlify Deployment Guide for Rentrobe

This guide covers multiple approaches to deploy your Flask application to Netlify.

## ⚠️ Important Note

Netlify is designed for static sites and serverless functions, not traditional Flask applications with databases. Your current Flask app requires significant adaptation for Netlify deployment.

## Option 1: Static Site Deployment (Recommended)

### Step 1: Prepare Your Project

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the static site**:
   ```bash
   python build_static.py
   ```

3. **Test locally**:
   ```bash
   # Serve the dist folder
   cd dist
   python -m http.server 8000
   ```

### Step 2: Deploy to Netlify

1. **Via Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify deploy --dir=dist --prod
   ```

2. **Via Netlify Dashboard**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   - Set build command: `python build_static.py`
   - Set publish directory: `dist`
   - Deploy!

### Step 3: Configure Environment Variables

In Netlify dashboard, go to Site settings > Environment variables:
- `SECRET_KEY`: Your Flask secret key
- `DATABASE_URL`: External database URL (if using one)

## Option 2: Serverless Functions Approach

### Step 1: Adapt Your Backend

1. **Move API logic to serverless functions**:
   - Copy your API routes to `netlify/functions/`
   - Adapt database connections for serverless environment
   - Use external database (PostgreSQL, MongoDB, etc.)

2. **Update frontend**:
   - Modify API calls to use Netlify functions
   - Update base URL to `/api/` instead of `/api/`

### Step 2: Deploy

1. **Build and deploy**:
   ```bash
   netlify deploy --prod
   ```

## Option 3: Hybrid Approach (Recommended for Production)

### Backend: Deploy Flask App Separately

1. **Deploy Flask app to**:
   - **Heroku**: `git push heroku main`
   - **Railway**: Connect GitHub repo
   - **Render**: Deploy from GitHub
   - **DigitalOcean App Platform**: Deploy from GitHub

2. **Set up external database**:
   - PostgreSQL on Heroku Postgres, Railway, or Supabase
   - Update `DATABASE_URL` environment variable

### Frontend: Deploy to Netlify

1. **Create frontend-only version**:
   - Extract HTML/CSS/JS from your Flask templates
   - Update API endpoints to point to your deployed backend
   - Deploy to Netlify

## Database Setup for Production

### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string
4. Update `DATABASE_URL` in your Flask app

### Option B: Railway PostgreSQL
1. Go to [railway.app](https://railway.app)
2. Create new project
3. Add PostgreSQL service
4. Get connection string

### Option C: Heroku Postgres
1. Add Heroku Postgres addon
2. Get `DATABASE_URL` from environment variables

## Environment Variables Setup

### For Flask App (Backend):
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
```

### For Netlify (Frontend):
```bash
REACT_APP_API_URL=https://your-backend-url.herokuapp.com
# or
REACT_APP_API_URL=https://your-backend-url.railway.app
```

## Step-by-Step Deployment (Option 3 - Recommended)

### 1. Deploy Backend to Railway

1. **Prepare your app**:
   ```bash
   # Create requirements.txt if not exists
   pip freeze > requirements.txt
   
   # Create Procfile
   echo "web: python app.py" > Procfile
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Connect GitHub repository
   - Add PostgreSQL service
   - Deploy!

3. **Get your backend URL**:
   - Copy the generated URL (e.g., `https://your-app.railway.app`)

### 2. Deploy Frontend to Netlify

1. **Create frontend build**:
   ```bash
   python build_static.py
   ```

2. **Update API endpoints** in your static files to point to your Railway backend

3. **Deploy to Netlify**:
   ```bash
   netlify deploy --dir=dist --prod
   ```

## Testing Your Deployment

1. **Test backend**: Visit `https://your-backend-url.railway.app/api/categories`
2. **Test frontend**: Visit your Netlify URL
3. **Test full flow**: Register, login, browse items

## Troubleshooting

### Common Issues:

1. **CORS errors**: Add CORS headers to your Flask app
2. **Database connection**: Ensure `DATABASE_URL` is set correctly
3. **Static files**: Check file paths in your templates
4. **Environment variables**: Verify all required variables are set

### Debug Commands:

```bash
# Check Flask app locally
python app.py

# Check static build
python build_static.py && cd dist && python -m http.server 8000

# Check Netlify functions locally
netlify dev
```

## Cost Considerations

- **Netlify**: Free tier available, paid plans for advanced features
- **Railway**: $5/month for hobby plan
- **Heroku**: $7/month for basic dyno
- **Database**: Varies by provider (Supabase free tier available)

## Security Considerations

1. **Environment variables**: Never commit secrets to Git
2. **CORS**: Configure properly for production
3. **HTTPS**: Both Netlify and Railway provide HTTPS by default
4. **Database**: Use connection pooling and proper indexing

## Next Steps

1. Choose your preferred deployment option
2. Set up external database
3. Deploy backend first
4. Deploy frontend
5. Test thoroughly
6. Set up monitoring and backups

For questions or issues, refer to the respective platform documentation or create an issue in your repository.
