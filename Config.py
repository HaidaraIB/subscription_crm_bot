import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID"))
    ERRORS_CHANNEL = int(os.getenv("ERRORS_CHANNEL"))
    REMINDERS_CHANNEL_ID = int(os.getenv("REMINDERS_CHANNEL_ID"))

    DB_PATH = os.getenv("DB_PATH")
    DB_POOL_SIZE = 20
    DB_MAX_OVERFLOW = 10

    TIMEZONE = os.getenv("TIMEZONE", "Asia/Riyadh")

    @staticmethod
    def _parse_reminder_check_hours() -> tuple[int, ...]:
        hours_str = os.getenv("REMINDER_CHECK_HOURS")
        if hours_str:
            return tuple(
                int(h.strip())
                for h in hours_str.split(",")
                if h.strip()
            )
        morning = int(os.getenv("REMINDER_CHECK_HOUR", "9"))
        evening = (morning + 12) % 24
        return (morning, evening) if morning != evening else (morning,)

    REMINDER_CHECK_HOURS = _parse_reminder_check_hours()
