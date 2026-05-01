from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
from flask import Flask
import threading
import time

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"

channel = "-1003633262234"

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay_between_edits = 10      # ⚠️ SAFE: 10 seconds between edits
max_edits_per_run = 50        # ⚠️ SAFE: Only 50 edits per deploy
# ==========================

app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

client = TelegramClient("safe_session", api_id, api_hash)

async def main():
    print("🚀 Starting safe link replacement...")
    edited_count = 0
    flood_occurred = False

    async for msg in client.iter_messages(channel):
        if edited_count >= max_edits_per_run:
            print(f"🛑 Reached safe limit ({max_edits_per_run}). Stopping.")
            break

        try:
            if msg.text and old_link in msg.text:
                new_text = msg.text.replace(old_link, new_link)
                
                # ⚠️ CRITICAL: Wait before edit
                await asyncio.sleep(delay_between_edits)
                
                await msg.edit(new_text)
                edited_count += 1
                print(f"✅ Edited msg {msg.id} | Total: {edited_count}")
                
                # Extra safety: longer wait every 10 edits
                if edited_count % 10 == 0:
                    print("⏸️ Taking 30 second break...")
                    await asyncio.sleep(30)

        except FloodWaitError as e:
            flood_occurred = True
            wait_time = e.seconds + 5  # Add 5 seconds extra safety
            print(f"⚠️ FLOOD WAIT: Sleeping {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            
            # If flood happens, stop after safe retry
            if wait_time > 60:
                print("🛑 Flood wait too long! Stopping to protect account.")
                break
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
            await asyncio.sleep(5)  # Safe delay on any error

    if not flood_occurred:
        print(f"🎉 Complete! Safely edited {edited_count} messages.")
    else:
        print(f"✅ Stopped safely after flood. Edited {edited_count} messages.")

def run_bot():
    with client:
        client.loop.run_until_complete(main())

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
