import re
from datetime import date, timedelta


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    return digits


def compute_end_date(start_date: date, duration_days: int) -> date:
    return start_date + timedelta(days=duration_days)


def renew_end_date(
    current_end: date,
    duration_days: int,
    *,
    from_today_if_expired: bool = True,
    today: date | None = None,
) -> date:
    if today is None:
        today = date.today()
    if from_today_if_expired and current_end < today:
        base = today
    else:
        base = current_end
    return base + timedelta(days=duration_days)


def days_until_expiry(end_date: date, today: date | None = None) -> int:
    if today is None:
        today = date.today()
    return (end_date - today).days


def parse_date(text: str) -> date | None:
    text = (text or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            from datetime import datetime

            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def strip_html_tags(text: str) -> str:
    """Plain text for Telegram <code>/<pre> blocks (no nested HTML formatting)."""
    return re.sub(r"<[^>]+>", "", text or "")


def parse_reminder_days(value: str) -> list[int]:
    days = []
    for part in (value or "3").split(","):
        part = part.strip()
        if part.isdigit():
            days.append(int(part))
    return sorted(set(days), reverse=True) if days else [3]
