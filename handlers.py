from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from config import (
    CHANNEL_URL,
    MAX_TEXT_LENGTH,
    SUPPORT_URL,
    SUPPORT_USERNAME,
)
from qr_service import generate_qr
from subscription import is_subscribed

CHECK_SUB = "check_sub"

WELCOME = (
    "👋 <b>Welcome to the QR Code Bot!</b>\n\n"
    "Send me any <b>link</b> or <b>text</b> and I'll turn it into a QR code."
)
JOIN_PROMPT = (
    "🔒 <b>Subscription required</b>\n\n"
    "To use this bot, please join our channel first, "
    "then tap <b>“I've joined”</b>."
)


def _join_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Join the channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ I've joined", callback_data=CHECK_SUB)],
        ]
    )


def _support_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"💬 Support @{SUPPORT_USERNAME}", url=SUPPORT_URL)]]
    )


async def _gate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Return True if the user may proceed; otherwise show the join prompt."""
    user = update.effective_user
    if await is_subscribed(context.bot, user.id):
        return True
    await update.effective_message.reply_text(
        JOIN_PROMPT, parse_mode=ParseMode.HTML, reply_markup=_join_keyboard()
    )
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await _gate(update, context):
        return
    await update.message.reply_text(
        WELCOME + "\n\n✍️ <b>Send your link or text now:</b>",
        parse_mode=ParseMode.HTML,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ Send any link or text and I'll reply with a QR code.\n"
        f"Need help? Contact @{SUPPORT_USERNAME}.",
        reply_markup=_support_keyboard(),
    )


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if await is_subscribed(context.bot, query.from_user.id):
        await query.answer("Thanks for joining! ✅")
        await query.edit_message_text(
            WELCOME + "\n\n✍️ <b>Send your link or text now:</b>",
            parse_mode=ParseMode.HTML,
        )
    else:
        await query.answer(
            "You haven't joined the channel yet. Please join first.",
            show_alert=True,
        )


async def text_to_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await _gate(update, context):
        return

    text = (update.message.text or "").strip()
    if not text:
        return

    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_text(
            f"⚠️ That's too long. Please keep it under {MAX_TEXT_LENGTH} characters."
        )
        return

    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_PHOTO)

    try:
        qr_image = await generate_qr(text)
    except Exception:
        await update.message.reply_text(
            "❌ I couldn't generate a QR code for that. Please try something shorter."
        )
        return

    await update.message.reply_photo(
        photo=qr_image,
        caption=(
            "✅ <b>Here's your QR code!</b>\n"
            "Scan it with your camera.\n\n"
            "Send another link or text to make a new one."
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=_support_keyboard(),
    )
