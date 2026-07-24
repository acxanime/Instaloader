# © Coded by @Dypixx

from pyrogram import Client, filters, enums
import aiohttp
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from var import IS_FSUB, ADMIN, CHNL_LINK, DUMP_CHANNEL, REEL_AUTO_DELETE
from .fsub import get_fsub
from .db import dy

# Safe Admin ID handling (list ya int dono ke liye)
ADMIN_ID = int(ADMIN[0]) if isinstance(ADMIN, list) else int(ADMIN)


async def fetch_insta_media(url: str):
    """Clean Instagram URL and fetch media using Cobalt & Fallback APIs."""
    # Extra tracking parameters (e.g., ?igsh=...) remove karke clean URL banayein
    clean_url = url.split("?")[0].strip()

    async with aiohttp.ClientSession() as session:
        # 1. Primary API: Cobalt API (Fast & Reliable)
        try:
            cobalt_payload = {
                "url": clean_url,
                "videoQuality": "max"
            }
            cobalt_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            async with session.post(
                "https://api.cobalt.tools/api/json",
                json=cobalt_payload,
                headers=cobalt_headers,
                timeout=12
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    media_url = data.get("url")
                    if media_url:
                        is_video = data.get("type") == "video"
                        return {
                            "result": {
                                "url": media_url,
                                "extension": "mp4" if is_video else "jpg",
                                "duration": "N/A",
                                "quality": "HD",
                                "formattedSize": "N/A"
                            }
                        }
        except Exception as e:
            print(f"Cobalt API Failed: {e}")

        # 2. Fallback API 1
        try:
            async with session.get(
                f"https://api.v2.instavideosdownloader.com/download?url={clean_url}",
                timeout=10
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if not data.get("error") and "result" in data:
                        return data
        except Exception as e:
            print(f"Fallback 1 Failed: {e}")

        # 3. Fallback API 2
        try:
            async with session.get(
                f"https://insta-dl.hazex.workers.dev/?url={clean_url}",
                timeout=10
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if not data.get("error") and "result" in data:
                        return data
        except Exception as e:
            print(f"Fallback 2 Failed: {e}")

    return None


@Client.on_message(filters.private & filters.text)
async def handle_direct_instagram_link(client, message):
    url = message.text.strip()
    if not url.startswith("https://www.instagram.com/"):
        return

    if await dy.is_user_banned(message.from_user.id):
        await message.reply(
            "**🚫 Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ.**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('🧑‍💻 Sᴜᴘᴘᴏʀᴛ', user_id=ADMIN_ID)]]
            )
        )
        return

    if IS_FSUB and not await get_fsub(client, message):
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    P = await message.reply("**⏳ Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ...**")

    data = await fetch_insta_media(url)
    if not data:
        await P.edit("**⚠️ Oᴏᴘs! Uɴᴀʙʟᴇ ᴛᴏ ᴘʀᴏᴄᴇss ᴛʜᴇ URL.\nPʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.**")
        return

    result = data.get("result", data)
    download_url = result.get("url")
    extension = str(result.get("extension", "")).lower()
    duration = result.get("duration", "N/A")
    quality = result.get("quality", "N/A")
    Size = result.get("formattedSize", "N/A")

    if not download_url:
        await P.edit("**⚠️ Uɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ.**")
        return

    BTN = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 ⱼₒᵢₙ ₒᵤᵣ 𝄴ₕₐₙₙₑₗ", url=CHNL_LINK)]])
    caption_common = f"<b>⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}\n📚 Qᴜᴀʟɪᴛʏ: {quality}\n📁 Sɪᴢᴇ: {Size}</b>"

    try:
        # Video/Reel Send
        if extension in ["mp4", "mkv"] or not extension:
            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
            t = await message.reply_video(
                video=download_url,
                caption=f"<b>🎭 Iɴsᴛᴀ Rᴇᴇʟ</b>\n\n{caption_common}",
                reply_markup=BTN
            )

            if DUMP_CHANNEL:
                await client.send_video(
                    DUMP_CHANNEL,
                    video=download_url,
                    caption=f"<b>🎭 Iɴsᴛᴀ Rᴇᴇʟ</b>\n\n{caption_common}\n\n📩 Bʏ: {message.from_user.mention} ({message.from_user.id})",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close‼️', callback_data='close')]])
                )

            await dy.update_user_activity(message.from_user.id)
            await P.delete()

            if REEL_AUTO_DELETE and REEL_AUTO_DELETE > 0:
                await asyncio.sleep(REEL_AUTO_DELETE)
                await t.delete()

        # Photo Send
        elif extension in ["jpg", "jpeg", "png"]:
            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            i = await message.reply_photo(
                photo=download_url,
                caption=f"<b>🎭 Iɴsᴛᴀ Pᴏsᴛ</b>\n\n{caption_common}",
                reply_markup=BTN
            )

            if DUMP_CHANNEL:
                await client.send_photo(
                    DUMP_CHANNEL,
                    photo=download_url,
                    caption=f"<b>🎭 Iɴsᴛᴀ Pᴏsᴛ</b>\n\n{caption_common}\n\n📩 Bʏ: {message.from_user.mention} ({message.from_user.id})",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close‼️', callback_data='close')]])
                )

            await dy.update_user_activity(message.from_user.id)
            await P.delete()

            if REEL_AUTO_DELETE and REEL_AUTO_DELETE > 0:
                await asyncio.sleep(REEL_AUTO_DELETE)
                await i.delete()

        else:
            await P.edit("**⚠️ Uɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ ғᴏʀᴍᴀᴛ!**")

    except Exception as e:
        print(f"Error sending media: {e}")
        await P.edit("**⚠️ Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴍᴇᴅɪᴀ. Tʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.**")


@Client.on_message(filters.command("insta") & filters.text)
async def download_instagram_content(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply("**⚠️ Use this command in a group.**")
        return

    if len(message.command) < 2:
        await message.reply(
            "**🔗 Please provide an Instagram post/reel link after the command.**\nExample: /insta https://www.instagram.com/reel/abc123/",
            quote=True
        )
        return

    url = message.text.split(None, 1)[1].strip()

    if await dy.is_user_banned(message.from_user.id):
        await message.reply(
            "**🚫 Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ.**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('🧑‍💻 Sᴜᴘᴘᴏʀᴛ', user_id=ADMIN_ID)]]
            ),
        )
        return

    if IS_FSUB and not await get_fsub(client, message):
        return

    if not url.startswith("https://www.instagram.com/"):
        await message.reply("**Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ ᴘᴏsᴛ/ʀᴇᴇʟ ʟɪɴᴋ 🤡**")
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    P = await message.reply("**⏳ Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ...**")

    data = await fetch_insta_media(url)
    if not data:
        await P.edit("**⚠️ Oᴏᴘs! Uɴᴀʙʟᴇ ᴛᴏ ᴘʀᴏᴄᴇss ᴛʜᴇ URL.\nPʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.**")
        return

    result = data.get("result", data)
    download_url = result.get("url")
    extension = str(result.get("extension", "")).lower()
    duration = result.get("duration", "N/A")
    quality = result.get("quality", "N/A")
    Size = result.get("formattedSize", "N/A")

    if not download_url:
        await P.edit("**⚠️ Uɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ.**")
        return

    BTN = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 ⱼₒᵢₙ ₒᵤᵣ 𝄴ₕₐₙₙₑₗ", url=CHNL_LINK)]])
    caption_common = f"<b>⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}\n📚 Qᴜᴀʟɪᴛʏ: {quality}\n📁 Sɪᴢᴇ: {Size}</b>"

    try:
        if extension in ["mp4", "mkv"] or not extension:
            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
            if DUMP_CHANNEL:
                await client.send_video(
                    DUMP_CHANNEL,
                    video=download_url,
                    caption=f"<b>🎭 Iɴsᴛᴀ Rᴇᴇʟ</b>\n\n{caption_common}\n\n📩 Bʏ: {message.from_user.mention} ({message.from_user.id})",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close‼️', callback_data='close')]])
                )
            await message.reply_video(
                video=download_url,
                caption=f"<b>🎭 Iɴsᴛᴀ Rᴇᴇʟ</b>\n\n{caption_common}",
                reply_markup=BTN
            )
        elif extension in ["jpg", "jpeg", "png"]:
            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            if DUMP_CHANNEL:
                await client.send_photo(
                    DUMP_CHANNEL,
                    photo=download_url,
                    caption=f"<b>🎭 Iɴsᴛᴀ Pᴏsᴛ</b>\n\n{caption_common}\n\n📩 Bʏ: {message.from_user.mention} ({message.from_user.id})",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close‼️', callback_data='close')]])
                )
            await message.reply_photo(
                photo=download_url,
                caption=f"<b>🎭 Iɴsᴛᴀ Pᴏsᴛ</b>\n\n{caption_common}",
                reply_markup=BTN
            )
        else:
            await P.edit("**⚠️ Uɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ ғᴏʀᴍᴀᴛ!**")
            return

        await dy.update_user_activity(message.from_user.id)
        await P.delete()

    except Exception as e:
        print(f"Error sending group media: {e}")
        await P.edit("**⚠️ Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴍᴇᴅɪᴀ.**")


"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.
"""
