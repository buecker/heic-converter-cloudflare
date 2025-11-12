# HEIC Converter Backend API

Python Flask API for converting HEIC images to JPEG. Supports all HEIC format variants using pillow-heif.

## Quick Deploy

### Railway (Recommended - Easiest)

1. **Via Railway CLI:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login and deploy
   railway login
   railway init
   railway up

   # Get your URL
   railway domain
   ```

2. **Via Railway Dashboard:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" > "Deploy from GitHub repo"
   - Select this repository/folder
   - Railway auto-detects Python and deploys
   - Your API will be at: `https://your-app.up.railway.app`

### Render

1. **Via Render Dashboard:**
   - Go to [render.com](https://render.com)
   - Click "New +" > "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn convert-server:app`
     - **Environment**: Python 3
   - Deploy

2. **Via Blueprint (render.yaml):**
   - Push `render.yaml` to your repo
   - In Render dashboard: "New" > "Blueprint"
   - Connect repo and deploy

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and launch
fly auth login
fly launch

# Deploy
fly deploy

# Get URL
fly status
```

## Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python convert-server.py

# Server runs on http://localhost:5001
```

## API Endpoints

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "message": "HEIC conversion server is running",
  "version": "1.0.0"
}
```

### POST /convert
Convert HEIC file to JPEG

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: File with key "file"

**Response:**
- Content-Type: image/jpeg
- Returns converted JPEG file

**Example:**
```bash
curl -X POST \
  -F "file=@image.heic" \
  http://localhost:5001/convert \
  -o converted.jpg
```

### GET /
API information

**Response:**
```json
{
  "name": "HEIC Conversion API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "convert": "/convert (POST with file)"
  }
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5001 |
| `FLASK_ENV` | Environment (development/production) | development |

## Production Deployment

The server is production-ready with:
- ✅ CORS enabled for cross-origin requests
- ✅ Gunicorn WSGI server (via Procfile)
- ✅ Environment-based port configuration
- ✅ Error handling and logging
- ✅ Health check endpoint

## Testing

Test the deployed API:

```bash
# Health check
curl https://your-app.railway.app/health

# Convert a file
curl -X POST \
  -F "file=@test.heic" \
  https://your-app.railway.app/convert \
  -o converted.jpg
```

## Costs

- **Railway**: Free tier (500 hours/month), then $5/month
- **Render**: Free tier (750 hours/month), then $7/month
- **Fly.io**: Free tier (3 shared VMs), then ~$2/month

## Troubleshooting

### Module not found errors
- Ensure all dependencies are in `requirements.txt`
- Rebuild/redeploy

### Port binding errors locally
- Check if port 5001 is in use: `lsof -ti:5001`
- Kill process or use different port

### CORS errors
- Backend has CORS enabled for all origins
- Check frontend is using correct backend URL

### Conversion fails
- Check logs on your hosting platform
- Verify pillow-heif is installed correctly
- Test with different HEIC files

## Support

For platform-specific help:
- Railway: [railway.app/help](https://railway.app/help)
- Render: [render.com/docs](https://render.com/docs)
- Fly.io: [fly.io/docs](https://fly.io/docs)
