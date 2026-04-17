# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

# Check if user is member of auth channel
async def is_user_member(client: Client, user_id: int) -> bool:
    """Check if user is a member of the auth channel"""
    auth_channel = config.AUTH_CHANNEL
    
    if not auth_channel:
        return True  # No auth channel configured
    
    try:
        # Remove @ if present in channel username
        if auth_channel.startswith('@'):
            auth_channel = auth_channel[1:]
        
        # Get channel
        channel = await client.get_chat(auth_channel)
        
        # Get user member status
        member = await client.get_chat_member(channel.id, user_id)
        
        # Check if user is not banned or left
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error checking auth channel membership: {e}")
        return False  # If error, assume not member

# Force subscribe handler decorator
def force_subscribe(func):
    """Decorator to force users to join auth channel"""
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        
        # Skip check for admins
        if user_id in config.ADMINS:
            return await func(client, message)
        
        # Check if user is member
        is_member = await is_user_member(client, user_id)
        
        if is_member:
            return await func(client, message)
        else:
            # Send force subscribe message
            auth_channel = config.AUTH_CHANNEL
            if auth_channel.startswith('@'):
                auth_channel = auth_channel[1:]
            
            # Create button
            channel_link = config.VERIFY_CHANNEL_LINK or f"https://t.me/{auth_channel}"
            
            buttons = InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 Join Channel", url=channel_link),
                InlineKeyboardButton("✅ Check Membership", callback_data="check_membership")
            ]])
            
            await message.reply_text(
                "**⚠️ Access Restricted**\n\n"
                f"You must join our channel to use this bot!\n\n"
                f"**Channel:** @{auth_channel}\n\n"
                "After joining, click the 'Check Membership' button.",
                reply_markup=buttons,
                disable_web_page_preview=True
            )
            return None
    return wrapper

# Callback handler for membership check
@Client.on_callback_query()
async def handle_membership_check(client: Client, callback_query):
    if callback_query.data == "check_membership":
        user_id = callback_query.from_user.id
        
        is_member = await is_user_member(client, user_id)
        
        if is_member:
            await callback_query.message.edit_text(
                "✅ **Verification Successful!**\n\n"
                "You have joined the channel. You can now use the bot.\n\n"
                "Send /start to continue."
            )
        else:
            auth_channel = config.AUTH_CHANNEL
            if auth_channel.startswith('@'):
                auth_channel = auth_channel[1:]
            
            channel_link = config.VERIFY_CHANNEL_LINK or f"https://t.me/{auth_channel}"
            
            await callback_query.answer(
                "You haven't joined the channel yet!", 
                show_alert=True
            )
            
            await callback_query.message.edit_reply_markup(
                InlineKeyboardMarkup([[
                    InlineKeyboardButton("📢 Join Channel", url=channel_link),
                    InlineKeyboardButton("✅ Check Membership", callback_data="check_membership")
                ]])
            )
