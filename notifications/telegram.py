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
        owner_id: int | None = None,
        owner_message: str | None = None,
    ) -> tuple[bool, bool]:
        customer_ok = False
        if customer.telegram_user_id:
            customer_ok = await self._send_message(
                bot, customer.telegram_user_id, message_body
            )

        owner_ok = False
        if owner_id and owner_id != customer.telegram_user_id and owner_message:
            owner_ok = await self._send_message(bot, owner_id, owner_message)

        return customer_ok, owner_ok
