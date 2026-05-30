import asyncio
from pyrogram import Client
from pyrogram.types import CallbackQuery

@Client.on_callback_query()
async def remove_btn_callback(client: Client, query: CallbackQuery):
    if query.data.startswith("remove_btn_"):
        try:
            parts = query.data.split("_")
            channel_id = int(parts[1])
            msg_id = int(parts[2])
            
            await client.edit_message_reply_markup(
                chat_id=channel_id,
                message_id=msg_id,
                reply_markup=None
            )
            await query.answer("✅ Buttons removed successfully!", show_alert=True)
            
            # Also update the log message to show it's done
            await query.message.edit_text(
                text=query.message.text + "\n\n✅ **Buttons have been removed from the original message.**"
            )
        except Exception as e:
            await query.answer(f"❌ Error: {str(e)}", show_alert=True)
