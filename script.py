from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
from flask import Flask
import threading
import time

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"
bot_token = "8458711873:AAHBiPv2XWDZ3WuGaRCZvejat8bEIfwVZkk"

# IMPORTANT: Use integer, not string!
channel = -1003633262234  # Removed quotes

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay_between_edits = 2
max_edits_per_run = 500
# ==========================

app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

@app.route('/health')
def health_check():
    return "Healthy", 200

async def main():
    print("🤖 Bot started! Editing messages...")
    edited_count = 0
    
    client = TelegramClient("bot_session", api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    bot_info = await client.get_me()
    print(f"✅ Bot logged in: @{bot_info.username}")
    print(f"✅ Channel ID: {channel}")
    
    async for msg in client.iter_messages(channel):
        if edited_count >= max_edits_per_run:
            print(f"🛑 Reached limit ({max_edits_per_run}). Stopping.")
            break

        try:
            if msg.text and old_link in msg.text:
                new_text = msg.text.replace(old_link, new_link)
                await asyncio.sleep(delay_between_edits)
                await msg.edit(new_text)
                edited_count += 1
                print(f"✅ Edited {msg.id} | Total: {edited_count}")

        except FloodWaitError as e:
            print(f"⏳ Flood wait: {e.seconds}s...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"⚠️ Error on msg {msg.id}: {e}")
            await asyncio.sleep(2)

    print(f"🎉 Done! Total edited: {edited_count} messages.")
    await client.disconnect()
    
    # Keep alive for Koyeb
    while True:
        await asyncio.sleep(60)

def run_bot():
    asyncio.run(main())

def run_flask():
    app.run(host='0.0.0.0', port=8080, threaded=True)

if __name__ == "__main__":
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=False)
    flask_thread.start()
    
    time.sleep(2)
    
    # Run bot
    run_bot()
