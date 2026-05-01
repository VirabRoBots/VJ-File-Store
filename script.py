from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from flask import Flask
import threading
import time
import os

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"
# NO bot_token - using user account

channel = -1003633262234

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay_between_edits = 10  # SAFER for user account
max_edits_per_run = 200   # Conservative limit
# ==========================

app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

async def main():
    print("👤 User account started! Editing messages...")
    edited_count = 0
    
    # First time: Will ask for phone number
    async with Client("user_session", api_id, api_hash) as client:
        me = await client.get_me()
        print(f"✅ Logged in as: {me.first_name} (@{me.username})")
        
        print("📡 Scanning channel messages...")
        
        async for msg in client.get_chat_history(channel, limit=5000):
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
                    
                    # Extra safety: pause every 20 edits
                    if edited_count % 20 == 0:
                        print("⏸️ Taking 30 second break...")
                        await asyncio.sleep(30)
                        
            except FloodWait as e:
                print(f"⏳ Flood wait: {e.value} seconds ({e.value//60} minutes)")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"⚠️ Error: {e}")
                await asyncio.sleep(5)
        
        print(f"🎉 Done! Edited {edited_count} messages")

def run_bot():
    asyncio.run(main())

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=False).start()
    time.sleep(2)
    run_bot()
