from datetime import date, timedelta
import sqlalchemy as sa
import models
from models.BotSettings import SETTING_REMINDER_DAYS
from common.subscription_utils import parse_reminder_days, normalize_phone
from common.lang_dicts import TEXTS


PAGE_SIZE = 10

def preview_customer_card(draft: dict, lang: models.Language) -> str:
    customer = models.Customer(
        name=draft.get("name"),
        phone=draft["service_username"],
        service_username=draft["service_username"],
        service_password=draft["service_password"],
        subscription_type=draft["subscription_type"],
        duration_days=draft["duration_days"],
        start_date=draft["start_date"],
        end_date=draft["end_date"],
        notes=draft.get("notes"),
        telegram_user_id=draft.get("telegram_user_id"),
    )
    return format_customer_card(customer, lang)

def format_customer_card(customer: models.Customer, lang: models.Language) -> str:
    is_active = customer.end_date >= date.today()
    status_key = "subs_status_active" if is_active else "subs_status_expired"
    return TEXTS[lang]["subs_customer_card"].format(
        name=customer.name or TEXTS[lang]["subs_name_none"],
        phone=customer.phone,
        service_username=customer.service_username,
        service_password=customer.service_password,
        subscription_type=customer.subscription_type,
        duration_days=customer.duration_days,
        start_date=customer.start_date.isoformat(),
        end_date=customer.end_date.isoformat(),
        status=TEXTS[lang][status_key],
        telegram_user_id=customer.telegram_user_id or TEXTS[lang]["subs_telegram_none"],
        notes=customer.notes or TEXTS[lang]["subs_notes_none"],
    )


def get_stats(session) -> dict:
    today = date.today()
    total = session.query(models.Customer).count()
    active = (
        session.query(models.Customer).filter(models.Customer.end_date >= today).count()
    )
    expired = total - active
    reminder_days = parse_reminder_days(
        models.BotSettings.get(session, SETTING_REMINDER_DAYS, "3")
    )
    max_days = max(reminder_days) if reminder_days else 3
    expiring_cutoff = today + timedelta(days=max_days)
    expiring = (
        session.query(models.Customer)
        .filter(
            models.Customer.end_date >= today,
            models.Customer.end_date <= expiring_cutoff,
        )
        .count()
    )
    return {
        "total": total,
        "active": active,
        "expired": expired,
        "expiring": expiring,
    }


def search_by_phone(session, phone: str):
    normalized = normalize_phone(phone)
    return (
        session.query(models.Customer).filter(models.Customer.phone == normalized).all()
    )


def search_by_username(session, username: str):
    username = (username or "").strip().lstrip("@")
    return (
        session.query(models.Customer)
        .filter(sa.func.lower(models.Customer.service_username) == username.lower())
        .all()
    )


def get_expiring_customers(session, page: int = 0):
    today = date.today()
    reminder_days = parse_reminder_days(
        models.BotSettings.get(session, SETTING_REMINDER_DAYS, "3")
    )
    max_days = max(reminder_days) if reminder_days else 3
    expiring_cutoff = today + timedelta(days=max_days)
    q = (
        session.query(models.Customer)
        .filter(
            models.Customer.end_date >= today,
            models.Customer.end_date <= expiring_cutoff,
        )
        .order_by(models.Customer.end_date.asc())
    )
    total = q.count()
    items = q.offset(page * PAGE_SIZE).limit(PAGE_SIZE).all()
    return items, total


def get_expired_customers(session, page: int = 0):
    today = date.today()
    q = (
        session.query(models.Customer)
        .filter(models.Customer.end_date < today)
        .order_by(models.Customer.end_date.desc())
    )
    total = q.count()
    items = q.offset(page * PAGE_SIZE).limit(PAGE_SIZE).all()
    return items, total


def clear_reminders_for_customer(session, customer_id: int) -> None:
    session.query(models.SubscriptionReminder).filter(
        models.SubscriptionReminder.customer_id == customer_id
    ).delete()
