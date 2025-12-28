# Authored By Certified Coders © 2025
import asyncio
import importlib
import os
import threading
from flask import Flask
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnnieXMedia import LOGGER, app, userbot
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.misc import sudo
from AnnieXMedia.plugins import ALL_MODULES
from AnnieXMedia.utils.database import get_banned_users, get_gbanned
from AnnieXMedia.utils.cookie_handler import fetch_and_store_cookies
from config import BANNED_USERS

# Create simple Flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running", 200

@flask_app.route('/health')
def health():
    return "OK", 200

def start_flask():
    """Start Flask in background"""
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

async def init():
    # Start Flask in separate thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    LOGGER("AnnieXMedia").info(f"🌐 Flask server started on port {os.environ.get('PORT', 8080)}")
    
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("❌ Assistant session not filled...")
        exit(1)

    try:
        await fetch_and_store_cookies()
        LOGGER("AnnieXMedia").info("✅ Cookies loaded")
    except Exception as e:
        LOGGER("AnnieXMedia").warning(f"⚠️ Cookie error: {e}")

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AnnieXMedia.plugins" + all_module)

    LOGGER("AnnieXMedia.plugins").info("✅ Modules loaded")

    await userbot.start()
    await StreamController.start()

    try:
        await StreamController.stream_call("http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
    except NoActiveGroupCall:
        LOGGER("AnnieXMedia").error("❌ Turn on voice chat in log group")
        exit(1)
    except:
        pass

    await StreamController.decorators()
    LOGGER("AnnieXMedia").info("✅ Bot Started")
    
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("AnnieXMedia").info("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(init())
