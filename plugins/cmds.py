# © Coded by @Dypixx

from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from var import *
import asyncio
from Script import txt
from .db import dy
from .fsub import get_fsub

# Admin ID helper (list ya int dono ke liye safety)
ADMIN_ID = int(ADMIN[0]) if isinstance(ADMIN, list) else int(ADMIN)

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    if await dy.is_user_banned(message.from_user.id):
        await message.reply(
            "**🚫 You are banned from using this bot**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support", user_id=ADMIN_ID)]])
        )
        return

    if await dy.get_user(message.from_user.id) is None:
        await dy.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, text="#NEw_USer\n\nUser: {}\nID: {}".format(message.from_user.mention, message.from_user.id))

    if IS_FSUB and not await get_fsub(client, message):
        return

    await message.reply_text(
        txt.START_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎭 Updates 🎭", url="https://t.me/ST_Rename_Update")],
            [InlineKeyboardButton("⚡ Help", callback_data="help"), InlineKeyboardButton("📚 About", callback_data="about")],
            [InlineKeyboardButton("🧑‍💻 Developer", user_id=ADMIN_ID)]
        ])
    )

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):
    try:
        msg = await message.reply_text("Wait a second!")
        if not message.reply_to_message:
            return await msg.edit("<b>Please reply to a message to broadcast.</b>")
        
        await msg.edit("Processing ...")
        completed = 0
        failed = 0
        to_copy_msg = message.reply_to_message
        users_list = await dy.get_all_users()
        total_users = len(users_list)

        for i, userDoc in enumerate(users_list):
            if i % 20 == 0 and i > 0:
                try:
                    await msg.edit(f"Total: {total_users}\nProcessed: {i}\nCompleted: {completed}\nFailed: {failed}")
                except Exception:
                    pass

            user_id = userDoc.get("user_id")
            if not user_id:
                continue

            try:
                await to_copy_msg.copy(int(user_id))
                completed += 1
                await asyncio.sleep(0.1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await to_copy_msg.copy(int(user_id))
                    completed += 1
                except Exception:
                    failed += 1
            except Exception as e:
                print(f"Error in broadcasting to {user_id}: {e}")
                failed += 1
                
        await msg.edit(f"Successfully Broadcasted\nTotal: {total_users}\nCompleted: {completed}\nFailed: {failed}")
    except Exception as e:
        print(f"Error in broadcast: {e}")
        await message.reply_text("An error occurred while broadcasting.")

@Client.on_message(filters.command("ban") & filters.private & filters.user(ADMIN))
async def ban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /ban user_id")
            return

        user_id = int(command_parts[1])
        reason = " ".join(command_parts[2:]) if len(command_parts) > 2 else None
        
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return

        if await dy.ban_user(user_id, reason):
            ban_message = f"User {user.mention} has been banned."
            if reason:
                ban_message += f"\nReason: {reason}"
            await message.reply_text(ban_message)
        else:
            await message.reply_text("Failed to ban user.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("unban") & filters.private & filters.user(ADMIN))
async def unban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /unban user_id")
            return

        user_id = int(command_parts[1])
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return

        if await dy.unban_user(user_id):
            await message.reply_text(f"User {user.mention} has been unbanned.")
        else:
            await message.reply_text("Failed to unban user or user was not banned.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMIN))
async def total_users(client, message):
    try:
        users = await dy.get_all_users()
        active_today = await dy.get_active_users_today()
        
        total_count = len(users)
        # Fix ZeroDivisionError
        active_rate = (active_today / total_count * 100) if total_count > 0 else 0.0

        await message.reply(
            f"📊 **Bot Statistics**\n\n👥 **Total Users:** `{total_count}`\n✅ **Active Today:** {active_today}\n📈 **Active Rate:** {active_rate:.1f}%",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Close", callback_data="close")]])
        )
    except Exception as e:
        r = await message.reply(f"❌ *Error:* `{str(e)}`")
        await asyncio.sleep(30)
        await r.delete()

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.
"""
