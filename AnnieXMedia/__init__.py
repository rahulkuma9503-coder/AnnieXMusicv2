# Authored By Certified Coders © 2025
from AnnieXMedia.core.bot import MusicBotClient
from AnnieXMedia.core.dir import StorageManager
from AnnieXMedia.core.git import git
from AnnieXMedia.core.userbot import Userbot
from AnnieXMedia.misc import dbb, heroku

from .logging import LOGGER

StorageManager()
git()
dbb()
heroku()

app = MusicBotClient()
userbot = Userbot()

# ===== WEB SERVER FOR RENDER =====
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health checks"""
    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Disable logging"""
        pass

def start_health_server():
    """Start a simple HTTP server for Render health checks"""
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    
    # Start server in a daemon thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    LOGGER("AnnieXMedia").info(f"🌐 Health server started on port {port}")
    return server
# ===== END WEB SERVER =====

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
