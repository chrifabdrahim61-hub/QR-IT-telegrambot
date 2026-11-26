import logging

from telegram import Bot
from telegram.constants import ChatMemberStatus
from telegram.error import TelegramError

from config import CHANNEL_USERNAME

logger = logging.getLogger(__name__)

_OK_STATUSES = {
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.OWNER,
}


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
    except TelegramError as exc:
        # Usually means the bot is not an admin of the channel.
        logger.error("Subscription check failed: %s", exc)
        return False

    if member.status in _OK_STATUSES:
        return True
    return member.status == ChatMemberStatus.RESTRICTED and bool(
        getattr(member, "is_member", False)
    )
