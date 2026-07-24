
# © Coded by @Dypixx

import os
from threading import Thread
from flask import Flask
from pyrogram.client import Client
from var import *

# --- Web Server for Koyeb Health Check ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live on Koyeb!", 200

def run_flask():
    # Koyeb par default port PORT variable se milta hai, nahi toh 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
# ----------------------------------------

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="reelloader",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} is started...")
        print("""
███████ ████████     ██████   ██████  ████████ ███████ 
██         ██        ██   ██ ██    ██    ██    ██      
███████    ██        ██████  ██    ██    ██    ███████ 
     ██    ██        ██   ██ ██    ██    ██         ██ 
███████    ██        ██████   ██████     ██    ███████ """)

    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        print(f"{me.first_name} is stopped...")


if __name__ == "__main__":
    # Web server ko background mein start karein
    keep_alive()
    # Bot ko start karein
    Bot().run()

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.
"""
