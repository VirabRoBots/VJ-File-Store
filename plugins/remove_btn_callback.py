import logging
from pyrogram import Client
from pyrogram.types import CallbackQuery

logger = logging.getLogger(__name__)

@Client.on_callback_query()
async def remove_btn_callback(client: Client, query: CallbackQuery):
    try:
        logger.info(f"Received callback: {query.data}")
        
        if query.data.startswith("remove_btn_"):
            logger.info(f"Processing remove_btn callback")
            parts = query.data.split("_")
            logger.info(f"Parts: {parts}")
            
            channel_id = int(parts[1])
            msg_id = int(parts[2])
            
            logger.info(f"Attempting to remove buttons from channel: {channel_id}, message: {msg_id}")
            
            await client.edit_message_reply_markup(
                chat_id=channel_id,
                message_id=msg_id,
                reply_markup=None
            )
            
            await query.answer("Buttons removed!", show_alert=True)
            logger.info(f"Successfully removed buttons")
        else:
            logger.info(f"Ignoring non-remove_btn callback: {query.data}")
            
    except Exception as e:
        logger.error(f"Error in remove_btn_callback: {e}", exc_info=True)
        await query.answer(f"Error: {str(e)}", show_alert=True)
