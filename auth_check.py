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
