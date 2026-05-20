from typing import Protocol
from telegram import Bot
import models


class ReminderNotifier(Protocol):
    async def send_expiry_reminder(
        self,
        bot: Bot,
        customer: models.Customer,
        message_body: str,
        *,
        owner_id: int | None = None,
        owner_message: str | None = None,
    ) -> tuple[bool, bool]:
        ...
