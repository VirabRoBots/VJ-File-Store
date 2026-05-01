from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
from flask import Flask
import threading

# ========= CONFIG =========
api_id = 14853951
api_hash = "0a33bc287078d4dace12aaecc8e73545"
bot_token = "8458711873:AAHBiPv2XWDZ3WuGaRCZvejat8bEIfwVZkk"

channel = "-1003633262234"

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay_between_edits = 2       # Bots are safer, can go faster
max_edits_per_run = 500       # Bot can do more
# ==========================

app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

# Use bot token instead of user login
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

async def main():
    print("🤖 Bot started! Editing messages...")
    edited_count = 0

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

def run_bot():
    with client:
        client.loop.run_until_complete(main())

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
