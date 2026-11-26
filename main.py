import asyncio
import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import handlers
from config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def on_error(update, context) -> None:
    logger.error("Unhandled error", exc_info=context.error)


def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is missing. Copy .env.example to .env and fill it in.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(
        CallbackQueryHandler(handlers.check_subscription, pattern=f"^{handlers.CHECK_SUB}$")
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.text_to_qr))
    app.add_error_handler(on_error)

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    # Python 3.14 no longer creates a default event loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()
