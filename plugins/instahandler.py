# © Coded by @Dypixx

from pyrogram import Client, filters, enums
import aiohttp
import asyncio
import yt_dlp
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from var import IS_FSUB, ADMIN, CHNL_LINK, DUMP_CHANNEL, REEL_AUTO_DELETE
from .fsub import get_fsub
from .db import dy

ADMIN_ID = int(ADMIN[0]) if isinstance(ADMIN, list) else int(ADMIN)


async def fetch_insta_media(url: str):
    """Fetch Instagram media directly using yt-dlp (No external API blockage)."""
    clean_url = url.split("?")[0].strip()

    # 1. Direct Extraction with yt-dlp
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def _extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(clean_url, download=False)

    try:
        info = await asyncio.to_thread(_extract)
        if info:
            # Handle single video or playlist/carousel
            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            download_url = info.get('url')
            ext = info.get('ext', 'mp4')
            duration_sec = info.get('duration')
            duration_str = f"{int(duration_sec)}s" if duration_sec else "N/A"

            if download_url:
                return {
                    "result": {
                        "url": download_url,
                        "extension": ext,
                        "duration": duration_str,
                        "quality": "HD",
                        "formattedSize": "N/A"
                    }
                }
    except Exception as e:
        print(f"yt-dlp Extraction Error: {e}")

    # 2. Fallback API (Agar yt-dlp me issue aaye)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.v2.instavideosdownloader.com/download?url={clean_url}", timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if not data.get("error") and "result" in data:
                        return data
    except Exception as e:
        print(f"Fallback API Error: {e}")

    return None
    
