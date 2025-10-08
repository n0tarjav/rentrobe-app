# Netlify Deployment Guide

## Your Flask App is Ready for Netlify! 🚀

### What's Been Set Up

✅ **Serverless Functions**: Your Flask API is configured as a Netlify serverless function  
✅ **Database**: SQLite database is included and will be initialized on first run  
✅ **Session Management**: Properly configured for Netlify's serverless environment  
✅ **CORS**: Configured for cross-origin requests  
✅ **Static Files**: All assets are properly built and ready  

### Deployment Steps

#### Option 1: Deploy via Netlify CLI (Recommended)

1. **Install Netlify CLI** (if not already installed):
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**:
   ```bash
   netlify login
   ```

3. **Deploy from the dist folder**:
   ```bash
   cd dist
   netlify deploy --prod
   ```

#### Option 2: Deploy via Netlify Dashboard

1. **Go to** [netlify.com](https://netlify.com) and login
2. **Click** "New site from Git"
3. **Connect** your GitHub repository
4. **Set build settings**:
   - Build command: `python build_static.py`
   - Publish directory: `dist`
   - Python version: `3.11`

#### Option 3: Drag & Drop Deployment

1. **Go to** [netlify.com](https://netlify.com) and login
2. **Drag and drop** the `dist` folder to the deploy area
3. **Your site will be live** in a few minutes!

### Environment Variables (Optional)

If you want to customize the secret key, add these in Netlify Dashboard > Site Settings > Environment Variables:

- `SECRET_KEY`: Your custom secret key (default is provided)
- `SESSION_COOKIE_SECURE`: `true` (for HTTPS)
- `SESSION_COOKIE_HTTPONLY`: `true`
- `SESSION_COOKIE_SAMESITE`: `Lax`

### Testing Your Deployment

1. **Visit your Netlify URL** (e.g., `https://your-site-name.netlify.app`)
2. **Test registration** with a new account
3. **Test login** with existing accounts
4. **Check console logs** for any issues

### Features Included

- ✅ User Registration & Login
- ✅ Session Management
- ✅ Database Persistence
- ✅ File Uploads
- ✅ Responsive Design
- ✅ All your existing features

### Troubleshooting

If you encounter issues:

1. **Check Netlify Function Logs**:
   - Go to Netlify Dashboard > Functions
   - Click on your function to see logs

2. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Look for any error messages

3. **Test API Endpoints**:
   - Visit `https://your-site.netlify.app/api/test`
   - Should return database status

### Database Notes

- The database is included in the deployment
- It will be initialized on first function call
- Demo user is automatically created
- All user data persists between function calls

### Support

If you need help:
1. Check the Netlify function logs
2. Test the API endpoints directly
3. Check browser console for errors

Your app is now ready for production! 🎉
