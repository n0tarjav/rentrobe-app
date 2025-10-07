# Netlify Deployment Guide for Rentrobe

This guide will help you deploy your Flask-based fashion rental platform to Netlify.

## Prerequisites

- A Netlify account (free at [netlify.com](https://netlify.com))
- Git repository with your code
- Python 3.11+ installed locally

## Step 1: Prepare Your Repository

1. **Commit all files to Git:**
   ```bash
   git add .
   git commit -m "Add Netlify deployment configuration"
   git push origin main
   ```

2. **Verify the following files are in your repository:**
   - `netlify.toml` - Netlify configuration
   - `requirements.txt` - Python dependencies
   - `build_static.py` - Build script
   - `netlify/functions/api.py` - Serverless function
   - `app.py` - Your Flask application
   - `templates/index.html` - Your frontend

## Step 2: Deploy to Netlify

### Option A: Deploy via Netlify Dashboard (Recommended)

1. **Go to [Netlify](https://app.netlify.com) and sign in**

2. **Click "New site from Git"**

3. **Connect your Git provider:**
   - Choose GitHub, GitLab, or Bitbucket
   - Authorize Netlify to access your repositories

4. **Select your repository:**
   - Find and select your `cursor` repository

5. **Configure build settings:**
   - **Build command:** `python build_static.py`
   - **Publish directory:** `dist`
   - **Python version:** `3.11`

6. **Set environment variables (if needed):**
   - Go to Site settings → Environment variables
   - Add any required environment variables:
     - `SECRET_KEY` (generate a secure random string)
     - `DATABASE_URL` (if using external database)

7. **Click "Deploy site"**

### Option B: Deploy via Netlify CLI

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify:**
   ```bash
   netlify login
   ```

3. **Initialize site:**
   ```bash
   netlify init
   ```

4. **Deploy:**
   ```bash
   netlify deploy --prod
   ```

## Step 3: Configure Database

Since Netlify Functions are stateless, you'll need to use an external database:

### Option A: Use SQLite with Netlify Functions (Limited)
- The current setup uses SQLite, which will reset on each function invocation
- This is only suitable for testing/demo purposes

### Option B: Use External Database (Recommended for Production)

1. **Set up a database service:**
   - **Free options:** Railway, Supabase, PlanetScale
   - **Paid options:** AWS RDS, Google Cloud SQL

2. **Update your environment variables:**
   - Add `DATABASE_URL` with your database connection string
   - Example: `postgresql://user:password@host:port/database`

3. **Update your Flask app:**
   - The app already supports `DATABASE_URL` environment variable
   - It will automatically use the external database when available

## Step 4: Test Your Deployment

1. **Visit your Netlify URL** (e.g., `https://your-site-name.netlify.app`)

2. **Test the main features:**
   - Browse items
   - User registration/login
   - Item creation
   - Rental requests

3. **Check the API endpoints:**
   - Visit `https://your-site-name.netlify.app/api/categories`
   - Should return JSON data

## Step 5: Custom Domain (Optional)

1. **Go to Site settings → Domain management**

2. **Add your custom domain:**
   - Click "Add custom domain"
   - Enter your domain name
   - Follow DNS configuration instructions

3. **Configure SSL:**
   - Netlify automatically provides SSL certificates
   - Enable "Force HTTPS" in Site settings

## Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check that Python 3.11 is selected
   - Verify all files are committed to Git
   - Check build logs in Netlify dashboard

2. **API not working:**
   - Verify `netlify/functions/api.py` is in the repository
   - Check function logs in Netlify dashboard
   - Ensure redirects are configured in `netlify.toml`

3. **Database issues:**
   - For production, use an external database
   - Check environment variables are set correctly
   - Verify database connection string format

4. **Static files not loading:**
   - Check that `build_static.py` copied files correctly
   - Verify `_redirects` and `_headers` files are created
   - Check file paths in your HTML/CSS

### Debug Steps:

1. **Check build logs:**
   - Go to Site settings → Build & deploy → Build logs

2. **Check function logs:**
   - Go to Functions tab in Netlify dashboard
   - Click on your function to see logs

3. **Test locally:**
   ```bash
   python build_static.py
   # Check the dist/ directory
   ```

## Performance Optimization

1. **Enable caching:**
   - Static assets are cached for 1 year
   - API responses are not cached
   - HTML files are not cached

2. **Image optimization:**
   - Consider using Netlify's image optimization
   - Compress images before upload

3. **CDN:**
   - Netlify automatically provides global CDN
   - No additional configuration needed

## Security Considerations

1. **Environment variables:**
   - Never commit sensitive data to Git
   - Use Netlify's environment variables for secrets

2. **CORS:**
   - API endpoints allow all origins (`*`)
   - Consider restricting for production

3. **File uploads:**
   - Currently limited to 16MB
   - Files are stored in Netlify's function storage (temporary)

## Monitoring

1. **Netlify Analytics:**
   - Basic analytics available in free tier
   - Upgrade for detailed analytics

2. **Function monitoring:**
   - Check function execution time and errors
   - Monitor function logs regularly

## Next Steps

1. **Set up monitoring:**
   - Consider adding error tracking (Sentry)
   - Set up uptime monitoring

2. **Backup strategy:**
   - Regular database backups
   - Code repository backups

3. **Scaling:**
   - Monitor function usage
   - Consider upgrading Netlify plan if needed

## Support

- **Netlify Documentation:** [docs.netlify.com](https://docs.netlify.com)
- **Netlify Community:** [community.netlify.com](https://community.netlify.com)
- **Function Logs:** Available in your Netlify dashboard

---

**Note:** This deployment uses Netlify Functions for the backend API. For high-traffic production applications, consider using a dedicated server or containerized deployment on platforms like Railway, Render, or AWS.
