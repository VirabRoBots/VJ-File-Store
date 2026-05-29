from urllib.parse import quote_plus
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from utils.file_properties import get_hash, get_name
from config import STREAM_MODE, URL, LOG_CHANNEL
from plugins.dbusers import db

ALLOWED_CHANNELS = [-1003907302256]

@Client.on_message(filters.channel & (filters.document | filters.video) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot: Client, broadcast: Message):
    if STREAM_MODE == False:
        return
    
    if broadcast.chat.id not in ALLOWED_CHANNELS:
        return
    
    try:
        file = broadcast.document or broadcast.video
        file_name = file.file_name if file else "Unknown File"
        
        msg = await broadcast.forward(chat_id=LOG_CHANNEL)
        
        stream = f"{URL}watch/{msg.id}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
        download = f"{URL}{msg.id}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🖥 WATCH NOW!", url=stream),
             InlineKeyboardButton("📥 DOWNLOAD", url=download)]
        ])
        
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=buttons
        )

    except FloodWait as w:
        await asyncio.sleep(w.value)
        await channel_receive_handler(bot, broadcast)
    except Exception as e:
        print(f"Error: {e}")
