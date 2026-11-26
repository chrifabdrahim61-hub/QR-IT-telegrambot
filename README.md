# QR Code Telegram Bot

Send a link or text → get a QR code back. Users must join the channel first.

## Features
- `/start` asks for a link or text
- Replies with a QR image + "Here's your QR code!" message
- Mandatory subscription to https://t.me/gifthubai (with "I've joined" re-check)
- Support button/tag: @vxgiyx

## Setup
1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. **Add your bot as an administrator of the channel `@gifthubai`** (required, otherwise Telegram won't let the bot verify members).
3. Install and configure:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then put your BOT_TOKEN inside
python main.py
```

## Structure
| File | Role |
|---|---|
| `main.py` | App entry point and handler registration |
| `handlers.py` | /start, /help, subscription button, text → QR |
| `subscription.py` | Channel membership check |
| `qr_service.py` | QR image generation |
| `config.py` | Settings loaded from `.env` |
