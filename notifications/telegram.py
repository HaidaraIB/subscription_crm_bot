from telegram import Bot
import models
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    async def _send_message(self, bot: Bot, chat_id: int, text: str) -> bool:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
            )
            return True
        except Exception as e:
            logger.error("Failed to send message to chat %s: %s", chat_id, e)
            return False

    async def send_expiry_reminder(
        self,
        bot: Bot,
        customer: models.Customer,
        message_body: str,
        *,
        reminders_channel_id: int | None = None,
        channel_message: str | None = None,
    ) -> tuple[bool, bool]:
        customer_ok = False
        if customer.telegram_user_id:
            customer_ok = await self._send_message(
                bot, customer.telegram_user_id, message_body
            )

        channel_ok = False
        if reminders_channel_id and channel_message:
            channel_ok = await self._send_message(
                bot, reminders_channel_id, channel_message
            )

        return customer_ok, channel_ok
