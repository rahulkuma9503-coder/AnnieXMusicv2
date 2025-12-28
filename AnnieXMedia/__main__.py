# Authored By Certified Coders © 2025
import asyncio
import importlib
import os
import threading
import sys
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

# Import and start Flask server immediately
from web_server import run_flask
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("✅ Web server started immediately")

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant session not filled")
        sys.exit(1)

    try:
        await fetch_and_store_cookies()
        LOGGER("AnnieXMedia").info("Cookies loaded")
    except Exception as e:
        LOGGER("AnnieXMedia").warning(f"Cookie error: {e}")

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

    LOGGER("AnnieXMedia.plugins").info("Modules loaded")

    await userbot.start()
    await StreamController.start()

    try:
        await StreamController.stream_call("http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
    except NoActiveGroupCall:
        LOGGER("AnnieXMedia").error("Turn on voice chat")
        sys.exit(1)
    except:
        pass

    await StreamController.decorators()
    LOGGER("AnnieXMedia").info("✅ Bot Started Successfully")
    
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("AnnieXMedia").info("Bot Stopped")

if __name__ == "__main__":
    asyncio.run(init())
