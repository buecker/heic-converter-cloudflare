# HEIC Converter - Cloudflare Pages Deployment

This is a split deployment setup:
- **Frontend**: Hosted on Cloudflare Pages (static HTML)
- **Backend**: Hosted on Railway/Render/Fly.io (Python Flask API)

## Quick Start

### 1. Deploy Frontend to Cloudflare Pages

#### Option A: Using Wrangler CLI (Recommended)

```bash
# Install dependencies
npm install

# Login to Cloudflare
npx wrangler login

# Deploy to Cloudflare Pages
npm run deploy
```

Your site will be live at: `https://heic-converter.pages.dev`

#### Option B: Using Cloudflare Dashboard

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to **Workers & Pages** > **Create application** > **Pages**
3. Connect your Git repository or upload files
4. Deploy the `heic-converter-cloudflare` directory

### 2. Deploy Backend (Choose One Platform)

You need to deploy the Python backend from the original `heic-converter` directory.

#### Option A: Railway (Easiest)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Go to the backend directory and deploy:
   ```bash
   cd ../heic-converter
   railway login
   railway init
   railway up
   ```

3. Get your backend URL:
   ```bash
   railway domain
   ```
   Example: `https://your-app.up.railway.app`

4. Update `index.html` in the Cloudflare deployment:
   ```javascript
   window.BACKEND_URL = 'https://your-app.up.railway.app';
   ```

5. Redeploy frontend with updated URL

#### Option B: Render

1. Go to [render.com](https://render.com) and sign up
2. Click **New +** > **Web Service**
3. Connect your GitHub repo or upload files
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn convert-server:app`
   - **Environment**: Python 3
5. Create `requirements.txt` in your backend directory:
   ```
   flask
   flask-cors
   pillow
   pillow-heif
   gunicorn
   ```
6. Deploy and get your URL (e.g., `https://your-app.onrender.com`)
7. Update `BACKEND_URL` in `index.html`

#### Option C: Fly.io

1. Install flyctl:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Deploy:
   ```bash
   cd ../heic-converter
   fly auth login
   fly launch
   fly deploy
   ```

3. Get URL: `fly status`
4. Update `BACKEND_URL` in `index.html`

### 3. Update Configuration

After deploying the backend, update `index.html`:

```javascript
window.BACKEND_URL = 'https://your-backend-url.com'; // Your deployed backend URL
```

Then redeploy the frontend:
```bash
npm run deploy
```

## Local Development

### Frontend Only
```bash
npm run dev
# Visit http://localhost:8000
```

### With Backend
1. Start backend (from `heic-converter` directory):
   ```bash
   cd ../heic-converter
   venv/bin/python convert-server.py
   ```

2. Open `index.html` in browser (already configured for localhost:5001)

## Architecture

```
┌─────────────────────────────────────────┐
│   Cloudflare Pages (Global CDN)        │
│   - Static HTML/JS/CSS                  │
│   - heic2any library (client-side)      │
└─────────────────┬───────────────────────┘
                  │
                  │ API Calls
                  ▼
┌─────────────────────────────────────────┐
│   Backend API (Railway/Render/Fly)      │
│   - Python Flask                        │
│   - pillow-heif converter               │
│   - Handles all HEIC variants           │
└─────────────────────────────────────────┘
```

## File Structure

```
heic-converter-cloudflare/
├── index.html          # Main application (deployed to Cloudflare)
├── wrangler.toml       # Cloudflare Pages config
├── package.json        # NPM dependencies
└── README.md          # This file

../heic-converter/      # Backend (deploy separately)
├── convert-server.py   # Flask API
├── venv/              # Python virtual environment
└── README.md          # Backend instructions
```

## Environment Variables (Backend)

If deploying to Railway/Render/Fly, set:

- `PORT`: Will be auto-set by the platform
- `FLASK_ENV`: Set to `production`

Update `convert-server.py` to use environment port:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
```

## Costs

- **Cloudflare Pages**: Free (unlimited requests)
- **Railway**: Free tier (500 hours/month, then $5/month)
- **Render**: Free tier (750 hours/month)
- **Fly.io**: Free tier (3 shared VMs)

## Troubleshooting

### CORS Errors
- Make sure Flask backend has `flask-cors` installed and configured
- Check backend URL is correct in `index.html`

### Backend Not Responding
- Check backend logs on your hosting platform
- Verify backend is running: `curl https://your-backend-url/health`

### Conversion Fails
- Check browser console for errors
- Verify both heic2any and backend are being tried
- Test backend directly: `curl -X POST -F "file=@test.heic" https://your-backend-url/convert`

## Custom Domain

To use your own domain (e.g., `heic.yourcompany.com`):

1. In Cloudflare Pages dashboard, go to your project
2. Click **Custom domains**
3. Add your domain and follow DNS instructions

## Support

For issues:
- Frontend issues: Check browser console (F12)
- Backend issues: Check your hosting platform's logs
- HEIC format issues: Backend should handle all variants via pillow-heif
# heic-converter-cloudflare
