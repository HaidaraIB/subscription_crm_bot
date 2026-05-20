import sqlalchemy as sa
from models.DB import Base
from datetime import datetime


class SubscriptionReminder(Base):
    __tablename__ = "subscription_reminders"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    customer_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reminder_kind = sa.Column(sa.String, nullable=False)
    sent_at = sa.Column(sa.DateTime, default=datetime.now)

    __table_args__ = (
        sa.UniqueConstraint(
            "customer_id", "reminder_kind", name="unique_customer_reminder_kind"
        ),
    )

    @staticmethod
    def make_kind(end_date, days_left: int) -> str:
        if days_left == 0:
            return f"expired_{end_date.isoformat()}"
        return f"days_{days_left}_{end_date.isoformat()}"
