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

# Create Flask app
flask_app = Flask(__name__)
bot_initialized = False

@flask_app.route('/')
def home():
    """Home route"""
    return "🚀 AnnieX Music Bot is running", 200

@flask_app.route('/health')
def health():
    """Health check endpoint for Render"""
    if bot_initialized:
        return "✅ AnnieX Music Bot is running", 200
    else:
        return "🔄 Bot is starting...", 503

@flask_app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return "pong", 200

def run_flask():
    """Run Flask server in a separate thread"""
    port = int(os.environ.get("PORT", 8080))
    LOGGER("AnnieXMedia").info(f"🌐 Starting Flask server on port {port}")
    flask_app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)

async def init():
    global bot_initialized
    
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    LOGGER("AnnieXMedia").info("🚀 Starting AnnieX Music Bot...")
    
    # Check for session strings
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("❌ Assistant session not filled, please fill a pyrogram session...")
        exit(1)

    # ✅ Try to fetch cookies at startup
    try:
        await fetch_and_store_cookies()
        LOGGER("AnnieXMedia").info("✅ YouTube cookies loaded successfully")
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

    LOGGER("AnnieXMedia.plugins").info("✅ Annie's modules loaded...")

    await userbot.start()
    await StreamController.start()

    try:
        await StreamController.stream_call("http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
    except NoActiveGroupCall:
        LOGGER("AnnieXMedia").error(
            "❌ Please turn on the voice chat of your log group/channel.\n\nAnnie bot stopped..."
        )
        exit(1)
    except Exception as e:
        LOGGER("AnnieXMedia").warning(f"⚠️ Stream call test failed: {e}")

    await StreamController.decorators()
    
    # Mark bot as initialized
    bot_initialized = True
    LOGGER("AnnieXMedia").info("✅ Annie Music Bot Started Successfully...")
    LOGGER("AnnieXMedia").info(f"✅ Flask server is running on port {os.environ.get('PORT', 8080)}")
    
    # Keep the bot running
    await idle()
    
    # Cleanup on exit
    bot_initialized = False
    await app.stop()
    await userbot.stop()
    LOGGER("AnnieXMedia").info("🛑 Stopping Annie Music Bot ...")

if __name__ == "__main__":
    # Start the bot
    asyncio.run(init())
