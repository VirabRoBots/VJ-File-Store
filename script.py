from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from flask import Flask
import threading
import time

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"
bot_token = "8458711873:AAHBiPv2XWDZ3WuGaRCZvejat8bEIfwVZkk"

channel = -1003633262234

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay_between_edits = 2
max_edits_per_run = 500
# ==========================

app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

async def main():
    print("🤖 Pyrogram Bot started!")
    edited_count = 0
    
    async with Client("pyro_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as client:
        print(f"✅ Bot logged in")
        
        async for msg in client.get_chat_history(channel):
            if edited_count >= max_edits_per_run:
                print(f"🛑 Reached limit. Stopping.")
                break
            
            try:
                if msg.text and old_link in msg.text:
                    new_text = msg.text.replace(old_link, new_link)
                    await asyncio.sleep(delay_between_edits)
                    await msg.edit_text(new_text)
                    edited_count += 1
                    print(f"✅ Edited {msg.id} | Total: {edited_count}")
            except FloodWait as e:
                print(f"⏳ Waiting {e.value}s...")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"⚠️ Error: {e}")
        
        print(f"🎉 Done! Edited {edited_count}")

def run_bot():
    asyncio.run(main())

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=False).start()
    time.sleep(2)
    run_bot()
