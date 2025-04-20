# © Coded by @Dypixx

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Script import txt
from var import ADMIN

@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    if query.data == "help":
        await query.message.edit_text(
            txt.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧑‍💻 Developer", user_id=int(ADMIN))],
                [InlineKeyboardButton("⬅️ Back", callback_data="back"), InlineKeyboardButton("📚 About", callback_data="about")]
            ]))
    elif query.data == "about":
        await query.message.edit_text(
            txt.ABOUT_TXT, 
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('⚡ Help', callback_data='help')],[
                    InlineKeyboardButton('🤖 Source Code', url="https://github.com/Dypixx/Instaloader"),
                    InlineKeyboardButton('⬅️ Back', callback_data='back')]]))
    elif query.data == "back":
        await query.message.edit_text(
            txt.START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎭 Updates 🎭", url="https://telegram.me/DypixxTech")],
                [InlineKeyboardButton("⚡ Help", callback_data="help"), InlineKeyboardButton("📚 About", callback_data="about")],
                [InlineKeyboardButton("🧑‍💻 Developer", user_id=int(ADMIN))]]))
    elif query.data == "close":
        await query.answer("Tʜᴀɴᴋs ғᴏʀ ᴄʟᴏsɪɴɢ ❤️", show_alert=True)
        await query.message.delete()

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit. 

"""
