import logging
from datetime import date

from telegram.ext import ContextTypes

from Config import Config
from common.lang_dicts import TEXTS, get_lang
from common.subscription_utils import parse_reminder_days
from models.BotSettings import (
    SETTING_RENEWAL_OFFER,
    SETTING_REMINDER_DAYS,
    SETTING_REMINDER_TEMPLATE,
)
from models.SubscriptionReminder import SubscriptionReminder
from notifications import get_notifier
import models

logger = logging.getLogger(__name__)


def _build_reminder_message(customer, days_left: int, session) -> str:
    offer = models.BotSettings.get(session, SETTING_RENEWAL_OFFER, "")
    template = models.BotSettings.get(session, SETTING_REMINDER_TEMPLATE, "")
    name = customer.name or customer.service_username
    return template.format(
        name=name,
        service_username=customer.service_username,
        end_date=customer.end_date.isoformat(),
        days_left=days_left,
        renewal_offer=offer,
    )


def _build_owner_reminder_message(
    customer, days_left: int, customer_message: str, lang
) -> str:
    texts = TEXTS[lang]
    telegram_id = (
        str(customer.telegram_user_id)
        if customer.telegram_user_id
        else texts["subs_telegram_none"]
    )
    return texts["subs_reminder_owner_message"].format(
        id=customer.id,
        name=customer.name or texts["subs_name_none"],
        phone=customer.phone,
        service_username=customer.service_username,
        service_password=customer.service_password,
        subscription_type=customer.subscription_type,
        duration_days=customer.duration_days,
        start_date=customer.start_date.isoformat(),
        end_date=customer.end_date.isoformat(),
        days_left=days_left,
        telegram_user_id=telegram_id,
        notes=customer.notes or texts["subs_notes_none"],
        customer_message=customer_message,
    )


async def check_expiring_subscriptions(context: ContextTypes.DEFAULT_TYPE):
    today = date.today()
    sent_to_customers = 0
    sent_to_owner = 0
    failed = 0
    notifier = get_notifier()

    with models.session_scope() as s:
        reminder_days = parse_reminder_days(
            models.BotSettings.get(s, SETTING_REMINDER_DAYS, "3")
        )
        customers = s.query(models.Customer).all()

        owner_lang = get_lang(Config.OWNER_ID)

        for customer in customers:
            days_left = (customer.end_date - today).days
            if days_left not in reminder_days:
                continue

            kind = SubscriptionReminder.make_kind(customer.end_date, days_left)
            existing = (
                s.query(SubscriptionReminder)
                .filter(
                    SubscriptionReminder.customer_id == customer.id,
                    SubscriptionReminder.reminder_kind == kind,
                )
                .first()
            )
            if existing:
                continue

            body = _build_reminder_message(customer, days_left, s)
            owner_body = _build_owner_reminder_message(
                customer, days_left, body, owner_lang
            )
            customer_ok, owner_ok = await notifier.send_expiry_reminder(
                bot=context.bot,
                customer=customer,
                message_body=body,
                owner_id=Config.OWNER_ID,
                owner_message=owner_body,
            )

            delivered = customer_ok or owner_ok
            if delivered:
                s.add(
                    SubscriptionReminder(
                        customer_id=customer.id,
                        reminder_kind=kind,
                    )
                )
                if customer_ok:
                    sent_to_customers += 1
                if owner_ok:
                    sent_to_owner += 1
            else:
                failed += 1

    if sent_to_customers or sent_to_owner or failed:
        try:
            summary = TEXTS[get_lang(Config.OWNER_ID)]["subs_reminder_summary"].format(
                sent_to_customers=sent_to_customers,
                sent_to_owner=sent_to_owner,
                failed=failed,
            )
            await context.bot.send_message(
                chat_id=Config.OWNER_ID,
                text=summary,
            )
        except Exception as e:
            logger.error("Failed to send reminder summary to owner: %s", e)

    logger.info(
        "Subscription reminders: sent_to_customers=%s sent_to_owner=%s failed=%s",
        sent_to_customers,
        sent_to_owner,
        failed,
    )
