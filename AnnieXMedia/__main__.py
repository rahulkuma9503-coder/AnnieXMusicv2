# Authored By Certified Coders © 2025
import asyncio
import importlib
import os
import sys
from aiohttp import web
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

# Global variable to track bot initialization
bot_initialized = False

async def health_check(request):
    """Health check endpoint for Render"""
    global bot_initialized
    if bot_initialized:
        return web.Response(text="✅ AnnieX Music Bot is running", status=200)
    else:
        return web.Response(text="🔄 Bot is starting...", status=503)

async def start_web_server():
    """Start aiohttp web server for Render"""
    # Get port from Render environment or use default
    port = int(os.environ.get("PORT", 10000))
    
    # Log port info
    LOGGER("AnnieXMedia").info(f"🌐 Starting web server on port {port}")
    LOGGER("AnnieXMedia").info(f"🌐 Server will be available at: 0.0.0.0:{port}")
    
    # Create app and routes
    app_web = web.Application()
    app_web.router.add_get('/', health_check)
    app_web.router.add_get('/health', health_check)
    app_web.router.add_get('/ping', lambda request: web.Response(text='pong'))
    
    # Configure the runner
    runner = web.AppRunner(app_web)
    await runner.setup()
    
    try:
        # Try to bind to the port
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        LOGGER("AnnieXMedia").info(f"✅ Web server successfully started on port {port}")
        LOGGER("AnnieXMedia").info(f"✅ Health check available at: http://0.0.0.0:{port}/health")
        return runner
    except OSError as e:
        LOGGER("AnnieXMedia").error(f"❌ Failed to start web server on port {port}: {e}")
        LOGGER("AnnieXMedia").info("⚠️ Trying alternative port 8080...")
        
        # Try alternative port
        try:
            site = web.TCPSite(runner, '0.0.0.0', 8080)
            await site.start()
            LOGGER("AnnieXMedia").info("✅ Web server started on port 8080")
            return runner
        except OSError as e2:
            LOGGER("AnnieXMedia").error(f"❌ Failed to start web server: {e2}")
            return None

async def init():
    global bot_initialized
    
    # Start web server FIRST (Render needs this immediately)
    LOGGER("AnnieXMedia").info("🚀 Starting web server for Render...")
    web_runner = await start_web_server()
    
    if not web_runner:
        LOGGER("AnnieXMedia").error("❌ Failed to start web server. Exiting...")
        exit(1)
    
    # Check for session strings
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("❌ Assistant session not filled, please fill a pyrogram session...")
        await web_runner.cleanup()
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
        await web_runner.cleanup()
        exit(1)
    except Exception as e:
        LOGGER("AnnieXMedia").warning(f"⚠️ Stream call test failed: {e}")

    await StreamController.decorators()
    
    # Mark bot as initialized
    bot_initialized = True
    LOGGER("AnnieXMedia").info("✅ Annie Music Bot Started Successfully...")
    LOGGER("AnnieXMedia").info("✅ Bot is now ready and listening for commands")
    
    # Keep the bot running
    await idle()
    
    # Cleanup on exit
    bot_initialized = False
    await app.stop()
    await userbot.stop()
    await web_runner.cleanup()
    LOGGER("AnnieXMedia").info("🛑 Stopping Annie Music Bot ...")


if __name__ == "__main__":
    # Clear any existing event loop (for Render compatibility)
    try:
        asyncio.get_event_loop().close()
    except:
        pass
    
    # Create new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(init())
    except KeyboardInterrupt:
        LOGGER("AnnieXMedia").info("🛑 Bot stopped by user")
    except Exception as e:
        LOGGER("AnnieXMedia").error(f"❌ Fatal error: {e}")
    finally:
        loop.close()
