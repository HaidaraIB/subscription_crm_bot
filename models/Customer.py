import sqlalchemy as sa
from models.DB import Base
from datetime import datetime, date
from common.subscription_utils import compute_end_date, renew_end_date, days_until_expiry


class Customer(Base):
    __tablename__ = "customers"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    phone = sa.Column(sa.String, nullable=False, index=True)
    service_username = sa.Column(sa.String, nullable=False, index=True)
    service_password = sa.Column(sa.String, nullable=False)
    subscription_type = sa.Column(sa.String, nullable=False, default="")
    duration_days = sa.Column(sa.Integer, nullable=False, default=30)
    start_date = sa.Column(sa.Date, nullable=False)
    end_date = sa.Column(sa.Date, nullable=False, index=True)
    notes = sa.Column(sa.Text, nullable=True)
    telegram_user_id = sa.Column(sa.BigInteger, nullable=True, index=True)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    def is_active(self, today: date | None = None) -> bool:
        if today is None:
            today = date.today()
        return self.end_date >= today

    def days_until_expiry(self, today: date | None = None) -> int:
        return days_until_expiry(self.end_date, today)

    def renew(self, duration_days: int, from_today_if_expired: bool = True) -> date:
        self.duration_days = duration_days
        self.end_date = renew_end_date(
            self.end_date,
            duration_days,
            from_today_if_expired=from_today_if_expired,
        )
        return self.end_date

    def set_dates_from_duration(self, start: date, duration_days: int) -> None:
        self.start_date = start
        self.duration_days = duration_days
        self.end_date = compute_end_date(start, duration_days)
