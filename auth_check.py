# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
import config  # ← ADD THIS IMPORT

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

# Add this middleware function to check ALL messages
async def check_auth_channel(client: Client, message: Message):
    """Check auth channel for all messages"""
    
    # Skip if auth channel mode is disabled
    if not config.AUTH_CHANNEL_MODE:
        return True
    
    # Skip if no auth channel configured
    if not config.AUTH_CHANNEL:
        return True
    
    user_id = message.from_user.id
    
    # Skip check for admins
    if user_id in config.ADMINS:
        return True
    
    # Check if user is member
    is_member = await is_user_member(client, user_id)
    
    if not is_member:
        # Prepare channel link
        auth_channel = config.AUTH_CHANNEL
        if auth_channel.startswith('@'):
            auth_channel = auth_channel[1:]
        
        channel_link = config.VERIFY_CHANNEL_LINK
        
        # Send force subscribe message
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton("📢 Join Channel", url=channel_link),
            InlineKeyboardButton("✅ Verify Membership", callback_data="check_membership")
        ]])
        
        # IMPORTANT: Only send if not already sent (check if message is the restriction message)
        if not message.text or not message.text.startswith("**🔒 Access Restricted**"):
            await message.reply_text(
                "**🔒 Access Restricted**\n\n"
                f"**You must join our channel to use this bot!**\n\n"
                "👉 Click the button below to join the channel"
                "After joining the channel, click the verify button below.",
                reply_markup=buttons,
                disable_web_page_preview=True
            )
        return False  # Not verified
    
    return True  # Verified
