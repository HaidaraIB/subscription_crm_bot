"""
Seed dummy customers to exercise check_expiring_subscriptions.

Default reminder_days is 3,1 — customers must have end_date = today+N for N in {3, 1}.

Re-run safe: removes prior rows whose phone starts with SEED_PHONE_PREFIX.

Usage (from project root):
    python scripts/seed_expiring_subscriptions_test.py
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

load_dotenv(os.path.join(ROOT, ".env"))

import models
from models.SubscriptionReminder import SubscriptionReminder

SEED_PHONE_PREFIX = "99900"


def _clear_previous_seed(session) -> int:
    customers = (
        session.query(models.Customer)
        .filter(models.Customer.phone.like(f"{SEED_PHONE_PREFIX}%"))
        .all()
    )
    for c in customers:
        session.delete(c)
    return len(customers)


def _add_customer(
    session,
    *,
    suffix: str,
    name: str,
    end_date: date,
    telegram_user_id: int | None,
    notes: str,
) -> models.Customer:
    today = date.today()
    duration = max((end_date - today).days, 1)
    start = end_date - timedelta(days=duration)
    phone = f"{SEED_PHONE_PREFIX}{suffix}"
    customer = models.Customer(
        name=name,
        phone=phone,
        service_username=f"seed_{suffix}",
        service_password="seed_pass",
        subscription_type="test",
        duration_days=duration,
        start_date=start,
        end_date=end_date,
        notes=notes,
        telegram_user_id=telegram_user_id,
    )
    session.add(customer)
    session.flush()
    return customer


def seed() -> None:
    models.init_db()
    today = date.today()
    in_3 = today + timedelta(days=3)
    in_1 = today + timedelta(days=1)
    in_7 = today + timedelta(days=7)
    yesterday = today - timedelta(days=1)

    with models.session_scope() as s:
        removed = _clear_previous_seed(s)
        if removed:
            print(f"Removed {removed} previous seed customer(s).")

        # Should match reminder_days 3 — fake TG id (send may fail; counts as failed)
        c_3d_send = _add_customer(
            s,
            suffix="01",
            name="Seed 3d — should notify",
            end_date=in_3,
            telegram_user_id=900000001,
            notes="Expect: sent or failed (not skipped)",
        )
        # Should match reminder_days 1
        _add_customer(
            s,
            suffix="02",
            name="Seed 1d — should notify",
            end_date=in_1,
            telegram_user_id=900000002,
            notes="Expect: sent or failed",
        )
        # 3 days left but no telegram — skipped
        _add_customer(
            s,
            suffix="03",
            name="Seed 3d — no Telegram",
            end_date=in_3,
            telegram_user_id=None,
            notes="Expect: skipped",
        )
        # 3 days left, reminder already recorded — job skips send
        c_3d_done = _add_customer(
            s,
            suffix="04",
            name="Seed 3d — already reminded",
            end_date=in_3,
            telegram_user_id=900000004,
            notes="Expect: no send (duplicate kind)",
        )
        s.add(
            SubscriptionReminder(
                customer_id=c_3d_done.id,
                reminder_kind=SubscriptionReminder.make_kind(in_3, 3),
            )
        )
        # Outside reminder window — job ignores
        _add_customer(
            s,
            suffix="05",
            name="Seed 7d — not in window",
            end_date=in_7,
            telegram_user_id=900000005,
            notes="Expect: ignored (days_left=7)",
        )
        _add_customer(
            s,
            suffix="06",
            name="Seed expired — not in window",
            end_date=yesterday,
            telegram_user_id=900000006,
            notes="Expect: ignored (days_left=-1)",
        )

    print(f"Seeded subscription test data (today={today.isoformat()}).")
    print(f"  Reminder targets: end_date {in_3.isoformat()} (3d), {in_1.isoformat()} (1d)")
    print("  Customers: 01–02 notify path, 03 skipped, 04 deduped, 05–06 ignored")
    print(f"  DB: {os.getenv('DB_PATH', '(set DB_PATH in .env)')}")


if __name__ == "__main__":
    seed()
