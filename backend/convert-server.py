#!/usr/bin/env python3
"""
Production-ready HEIC to JPEG conversion server
Supports deployment to Railway, Render, Fly.io, etc.

Environment Variables:
    PORT: Server port (default: 5001)
    FLASK_ENV: Environment (production/development)
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
import pillow_heif
import io
import os

app = Flask(__name__)

# Enable CORS for all origins (configure more restrictively in production if needed)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

@app.route('/convert', methods=['POST', 'OPTIONS'])
def convert_heic():
    """Convert uploaded HEIC file to JPEG"""
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return '', 204

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read HEIC file
        heic_data = file.read()

        # Open and convert to JPEG
        image = Image.open(io.BytesIO(heic_data))

        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')

        # Save as JPEG
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=90, optimize=True)
        output.seek(0)

        # Generate output filename
        filename = os.path.splitext(file.filename)[0] + '.jpg'

        return send_file(
            output,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"Conversion error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'HEIC conversion server is running',
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API info"""
    return jsonify({
        'name': 'HEIC Conversion API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'convert': '/convert (POST with file)'
        }
    })

if __name__ == '__main__':
    # Get port from environment variable (for Railway, Render, etc.)
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'

    print("=" * 60)
    print("HEIC Conversion Server")
    print("=" * 60)
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Port: {port}")
    print(f"Health check: http://0.0.0.0:{port}/health")
    print(f"Conversion endpoint: http://0.0.0.0:{port}/convert")
    print("=" * 60)

    # Use 0.0.0.0 to allow external connections (required for cloud platforms)
    app.run(host='0.0.0.0', port=port, debug=debug)
