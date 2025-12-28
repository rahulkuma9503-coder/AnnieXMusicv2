#!/usr/bin/env python3
"""
Simple entry point for Render that starts web server first
"""
import os
import threading
import time
from flask import Flask

# Start Flask IMMEDIATELY
app = Flask(__name__)

@app.route('/')
def home():
    return "AnnieX Bot", 200

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

# Start Flask in background thread
thread = threading.Thread(target=run_flask, daemon=True)
thread.start()

# Wait for Flask to initialize
time.sleep(2)

# Now import and run your bot
import asyncio
from AnnieXMedia.__main__ import init

if __name__ == "__main__":
    asyncio.run(init())
