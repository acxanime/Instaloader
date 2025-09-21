# © Coded by @Dypixx
import os
from typing import List

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN = int(os.getenv("ADMIN", "6692613520"))

CHNL_LINK = os.getenv("CHNL_LINK", "https://t.me/ST_Rename_Update")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002320080278"))
DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL", "-1002956078693"))

DB_URI = os.getenv("DB_URI", "mongodb+srv://sitaratoons:sitaratoons@cluster0.98nq3.mongodb.net/?retryWrites=true&w=majority") #MongoDB URL
DB_NAME = os.getenv("DB_NAME", "Cluster0")

IS_FSUB = bool(os.environ.get("FSUB", True)) # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002355394644").split())) # Add Multiple channel id

REEL_AUTO_DELETE = int(os.getenv("REEL_AUTO_DELETE", "10800")) #10min

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.

"""
