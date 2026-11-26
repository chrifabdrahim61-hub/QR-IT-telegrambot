import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "gifthubai").lstrip("@").strip()
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "vxgiyx").lstrip("@").strip()

CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME}"
SUPPORT_URL = f"https://t.me/{SUPPORT_USERNAME}"

# Longest text accepted for a QR code (keeps the code scannable)
MAX_TEXT_LENGTH = 1000
