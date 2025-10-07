# 🚀 Step-by-Step Deployment Guide for Rentrobe

## Prerequisites
- GitHub account
- Netlify account (free)
- Railway account (free) or Heroku account
- Git installed on your computer

---

## Phase 1: Prepare Your Code for Deployment

### Step 1: Initialize Git Repository (if not already done)
```bash
# Navigate to your project folder
cd "E:\Personal files\Yapperrr\Wearhouse\cursor"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit - Rentrobe Flask app"
```

### Step 2: Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `rentrobe-app`
4. Make it **Public** (required for free Netlify)
5. **Don't** initialize with README (you already have files)
6. Click "Create repository"

### Step 3: Push Code to GitHub
```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/rentrobe-app.git

# Push to GitHub
git push -u origin main
```
*Replace `YOUR_USERNAME` with your actual GitHub username*

---

## Phase 2: Deploy Backend to Railway

### Step 4: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 5: Deploy Flask App to Railway
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `rentrobe-app` repository
4. Railway will automatically detect it's a Python app

### Step 6: Add Database to Railway
1. In your project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will create a PostgreSQL database
4. Copy the `DATABASE_URL` from the database service

### Step 7: Configure Environment Variables
1. Click on your Flask app service
2. Go to "Variables" tab
3. Add these environment variables:
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=postgresql://... (copy from database service)
   FLASK_ENV=production
   PORT=8000
   ```

### Step 8: Deploy and Get Backend URL
1. Railway will automatically deploy your app
2. Wait for deployment to complete (green checkmark)
3. Click on your app service
4. Go to "Settings" → "Domains"
5. Copy your app URL (e.g., `https://rentrobe-app-production.up.railway.app`)

---

## Phase 3: Deploy Frontend to Netlify

### Step 9: Create Netlify Account
1. Go to [netlify.com](https://netlify.com)
2. Click "Sign up" → "Sign up with GitHub"
3. Authorize Netlify to access your GitHub

### Step 10: Build Static Site
```bash
# Make sure you're in your project directory
cd "E:\Personal files\Yapperrr\Wearhouse\cursor"

# Install Python dependencies
pip install -r requirements.txt

# Build static site
python build_static.py
```

### Step 11: Deploy to Netlify via Dashboard
1. In Netlify dashboard, click "New site from Git"
2. Choose "GitHub" as provider
3. Select your `rentrobe-app` repository
4. Configure build settings:
   - **Build command**: `python build_static.py`
   - **Publish directory**: `dist`
   - **Python version**: `3.11`
5. Click "Deploy site"

### Step 12: Configure Netlify Environment Variables
1. Go to Site settings → Environment variables
2. Add these variables:
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=postgresql://... (same as Railway)
   ```

---

## Phase 4: Connect Frontend to Backend

### Step 13: Update API Endpoints
You need to modify your static site to point to your Railway backend:

1. **Find your Netlify site URL** (e.g., `https://amazing-rentrobe-123456.netlify.app`)

2. **Update the build script** to use your Railway backend URL:
   ```python
   # In build_static.py, add this at the top
   BACKEND_URL = "https://your-railway-app.up.railway.app"
   ```

3. **Rebuild and redeploy**:
   ```bash
   python build_static.py
   # Netlify will automatically redeploy
   ```

---

## Phase 5: Test Your Deployment

### Step 14: Test Backend API
1. Open your Railway URL in browser
2. Test these endpoints:
   - `https://your-railway-app.up.railway.app/api/categories`
   - `https://your-railway-app.up.railway.app/api/items`

### Step 15: Test Frontend
1. Open your Netlify URL
2. Test the complete flow:
   - Browse items
   - Register new user
   - Login
   - Create item listing

---

## Phase 6: Custom Domain (Optional)

### Step 16: Add Custom Domain to Netlify
1. In Netlify dashboard, go to Site settings → Domain management
2. Click "Add custom domain"
3. Enter your domain (e.g., `rentrobe.com`)
4. Follow DNS configuration instructions

### Step 17: Add Custom Domain to Railway
1. In Railway dashboard, go to your app service
2. Go to Settings → Domains
3. Add your custom domain
4. Configure DNS records

---

## Troubleshooting Common Issues

### Issue 1: Build Fails on Netlify
**Solution**: Check build logs in Netlify dashboard
```bash
# Test build locally first
python build_static.py
```

### Issue 2: Database Connection Error
**Solution**: Verify DATABASE_URL is correct
```bash
# Test database connection
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database connected!')"
```

### Issue 3: CORS Errors
**Solution**: Add CORS headers to your Flask app
```python
# Add to app.py
from flask_cors import CORS
CORS(app)
```

### Issue 4: Static Files Not Loading
**Solution**: Check file paths in templates
```bash
# Verify static files exist
ls -la dist/static/
```

---

## Cost Breakdown

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| **Netlify** | 100GB bandwidth/month | $19/month for Pro |
| **Railway** | $5 credit/month | $5/month for Hobby |
| **GitHub** | Free for public repos | Free |
| **Total** | **$0-5/month** | **$24-29/month** |

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS (automatic with Netlify/Railway)
- [ ] Set up proper CORS headers
- [ ] Regular database backups
- [ ] Monitor usage and costs

---

## Next Steps After Deployment

1. **Set up monitoring**: Add error tracking (Sentry)
2. **Add analytics**: Google Analytics or similar
3. **Set up backups**: Regular database backups
4. **Performance optimization**: CDN, caching
5. **SSL certificates**: Automatic with Netlify/Railway

---

## Quick Commands Reference

```bash
# Local development
python app.py

# Build static site
python build_static.py

# Test static site locally
cd dist && python -m http.server 8000

# Deploy to Railway
git push origin main  # Railway auto-deploys

# Deploy to Netlify
git push origin main  # Netlify auto-deploys

# Check deployment status
railway status
netlify status
```

---

## Support Resources

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Netlify Docs**: [docs.netlify.com](https://docs.netlify.com)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)

---

**🎉 Congratulations!** Your Rentrobe app should now be live on the internet!

**Frontend**: `https://your-app-name.netlify.app`
**Backend**: `https://your-app-name.up.railway.app`

