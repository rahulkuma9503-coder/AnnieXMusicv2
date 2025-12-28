# Authored By Certified Coders © 2025
from AnnieXMedia.core.bot import MusicBotClient
from AnnieXMedia.core.dir import StorageManager
from AnnieXMedia.core.git import git
from AnnieXMedia.core.userbot import Userbot
from AnnieXMedia.misc import dbb, heroku
from flask import Flask

from .logging import LOGGER

StorageManager()
git()
dbb()
heroku()

app = MusicBotClient()
userbot = Userbot()

# Create Flask web app for Render
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running", 200

@web_app.route('/health')
def health():
    return "OK", 200

@web_app.route('/ping')
def ping():
    return "pong", 200

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
