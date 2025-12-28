"""
Simple Flask server for Render health checks
"""
from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ AnnieX Music Bot is running", 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "pong", 200

def run_flask():
    """Run Flask server on Render's port"""
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Starting Flask server on port {port}...")
    # Use waitress for production
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    run_flask()
