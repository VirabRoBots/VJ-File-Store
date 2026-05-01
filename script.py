from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio

# ========= CONFIG =========
api_id = 14853951  # 🔁 replace
api_hash = "0a33bc287078d4dace12aaecc8e73545"  # 🔁 replace

channel = "-1003633262234"  # @username or -100xxxx

old_link = "https://t.me/+VO7e3SdukyczOTE9"
new_link = "https://t.me/+M3LkAUujeR5jNzQ9"

delay = 5          # ✅ safe delay (seconds)
max_edits = 200    # ✅ limit per run
# ==========================

client = TelegramClient("safe_session", api_id, api_hash)

async def main():
    print("🚀 Script started...")
    edited_count = 0

    async for msg in client.iter_messages(channel):
        if edited_count >= max_edits:
            print(f"🛑 Reached limit ({max_edits}). Stop safely.")
            break

        try:
            if msg.text and old_link in msg.text:
                new_text = msg.text.replace(old_link, new_link)

                await msg.edit(new_text)
                edited_count += 1

                print(f"✅ Edited: {msg.id} | Total: {edited_count}")
                await asyncio.sleep(delay)

        except FloodWaitError as e:
            print(f"⏳ Flood wait: {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)

        except Exception as e:
            print(f"⚠️ Error at {msg.id}: {e}")
            await asyncio.sleep(3)

    print(f"🎉 Done! Total edited: {edited_count}")

with client:
    client.loop.run_until_complete(main())
