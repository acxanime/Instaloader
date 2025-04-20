# © Coded by @Dypixx

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from var import AUTH_CHANNEL
from pyrogram import Client
from pyrogram.types import Message
from typing import List
from pyrogram.errors import UserNotParticipant

async def get_fsub(bot: Client, message: Message) -> bool:
    dy = await bot.get_me()
    target_channel_id = AUTH_CHANNEL
    user_id = message.from_user.id
    try:
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        channel_link: str = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("Join Channel", url=channel_link)
        try_again_button = InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{dy.username}?start=start")
        keyboard: List[List[InlineKeyboardButton]] = [[join_button],[try_again_button]]
        await message.reply(
            f"**🎭 {message.from_user.mention}, ᴀꜱ ɪ ꜱᴇᴇ, ʏᴏᴜ ʜᴀᴠᴇɴ’ᴛ ᴊᴏɪɴᴇᴅ ᴍʏ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ.\nᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.**",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    return True

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.

"""
