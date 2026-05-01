from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
from flask import Flask
import os

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"
bot_token = "8458711873:AAHBiPv2XWDZ3WuGaRCZvejat8bEIfwVZkk"

channel = "-1003633262234"

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
    
    print(f"✅ Bot logged in: {await client.get_me()}")
    
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
            print(f"⏳ Waiting {e.seconds}s...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            await asyncio.sleep(2)

    print(f"🎉 Done! Edited {edited_count} messages.")
    await client.disconnect()

# Run everything in the same event loop
if __name__ == "__main__":
    # Run the bot first
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    
    # Then start Flask (but it won't run if bot finished)
    # For Koyeb, we need Flask to keep running
    app.run(host='0.0.0.0', port=8080)
