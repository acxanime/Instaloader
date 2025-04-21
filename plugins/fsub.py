# © Coded by @Dypixx

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from var import AUTH_CHANNELS
from pyrogram import Client
from pyrogram.types import Message
from typing import List
from pyrogram.errors import UserNotParticipant

async def get_fsub(bot: Client, message: Message) -> bool:
    dy = await bot.get_me()
    user_id = message.from_user.id
    not_joined_channels = []
    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)
            invite_link = chat.invite_link or await bot.export_chat_invite_link(channel_id)
            not_joined_channels.append((chat.title, invite_link))
    if not_joined_channels:
        join_buttons = []
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    button_text = f"{i + j + 1}. {title}"
                    row.append(InlineKeyboardButton(button_text, url=link))
            join_buttons.append(row)
        join_buttons.append([InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{dy.username}?start=start")])
        await message.reply(f"**🎭 {message.from_user.mention}, ᴀꜱ ɪ ꜱᴇᴇ, ʏᴏᴜ ʜᴀᴠᴇɴ’ᴛ ᴊᴏɪɴᴇᴅ ᴍʏ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ.\nᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.**",
                            reply_markup=InlineKeyboardMarkup(join_buttons),)
        return False
    return True

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.

"""
