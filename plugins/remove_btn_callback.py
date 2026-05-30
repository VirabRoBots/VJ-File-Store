from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import LOG_CHANNEL

@Client.on_callback_query()
async def remove_btn_callback(client: Client, query: CallbackQuery):
    if query.data.startswith("remove_btn_"):
        parts = query.data.split("_")
        channel_id = int(parts[1])
        msg_id = int(parts[2])
        
        await client.edit_message_reply_markup(
            chat_id=channel_id,
            message_id=msg_id,
            reply_markup=None
        )
        await query.answer("Buttons removed!", show_alert=True)
