import sqlalchemy as sa
from models.DB import Base
from datetime import datetime

DEFAULT_RENEWAL_OFFER_AR = (
    "عرض التجديد:\n"
    "• اشتراك شهر: خصم 10%\n"
    "• اشتراك 3 أشهر: شهر إضافي مجاناً\n"
    "تواصل معنا لتجديد اشتراكك."
)

SETTING_RENEWAL_OFFER = "renewal_offer_text"
SETTING_REMINDER_DAYS = "reminder_days_before"
SETTING_DEFAULT_DURATION = "default_duration_days"
SETTING_REMINDER_TEMPLATE = "reminder_message_template"

DEFAULT_REMINDER_TEMPLATE_AR = (
    "مرحباً {name}\n\n"
    "تنبيه: اشتراكك ({service_username}) سينتهي خلال <b>{days_left}</b> يوم/أيام.\n"
    "تاريخ الانتهاء: <b>{end_date}</b>\n\n"
    "{renewal_offer}"
)

DEFAULTS = {
    SETTING_RENEWAL_OFFER: DEFAULT_RENEWAL_OFFER_AR,
    SETTING_REMINDER_DAYS: "3,1",
    SETTING_DEFAULT_DURATION: "30",
    SETTING_REMINDER_TEMPLATE: DEFAULT_REMINDER_TEMPLATE_AR,
}


class BotSettings(Base):
    __tablename__ = "bot_settings"

    key = sa.Column(sa.String, primary_key=True)
    value = sa.Column(sa.Text, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def get(session, key: str, default: str | None = None) -> str:
        row = session.get(BotSettings, key)
        if row:
            return row.value
        return default if default is not None else DEFAULTS.get(key, "")

    @staticmethod
    def set(session, key: str, value: str) -> None:
        row = session.get(BotSettings, key)
        if row:
            row.value = value
        else:
            session.add(BotSettings(key=key, value=value))

    @staticmethod
    def seed_defaults(session) -> None:
        for key, value in DEFAULTS.items():
            if not session.get(BotSettings, key):
                session.add(BotSettings(key=key, value=value))
