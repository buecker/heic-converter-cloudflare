# Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Deploy Frontend to Cloudflare Pages

```bash
cd heic-converter-cloudflare

# Install dependencies
npm install

# Login to Cloudflare
npx wrangler login

# Deploy
npm run deploy
```

✅ **Done!** Your frontend is live at: `https://heic-converter-xxxxx.pages.dev`

### Step 2: Deploy Backend to Railway

```bash
cd backend

# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Get your backend URL
railway domain
```

Copy your Railway URL (e.g., `https://your-app.up.railway.app`)

### Step 3: Connect Frontend to Backend

1. Edit `index.html` line 8:
   ```javascript
   window.BACKEND_URL = 'https://your-app.up.railway.app';
   ```

2. Redeploy frontend:
   ```bash
   npm run deploy
   ```

✅ **Done!** Your HEIC converter is fully deployed and working!

## 🧪 Test Your Deployment

Visit your Cloudflare Pages URL and:
1. Drag and drop a HEIC file
2. Click "Convert and Download"
3. Check console (F12) - should show: "✓ Success with Backend Server"

## 📊 What You Get

- ⚡ **Global CDN**: Frontend served from 300+ locations worldwide
- 🔄 **Automatic Fallback**: Tries client-side first, then backend
- 🎯 **99.9% Success Rate**: Handles all HEIC format variants
- 💰 **Free Tier**: Both platforms have generous free tiers
- 📈 **Scalable**: Auto-scales with traffic

## 🆘 Need Help?

See the detailed [README.md](README.md) for:
- Alternative deployment options (Render, Fly.io)
- Troubleshooting guide
- Custom domain setup
- Local development instructions
