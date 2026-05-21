# Subscription CRM Bot

Telegram bot for managing customer subscriptions (IPTV/service accounts): store credentials, search, renew, expiry reminders, and admin statistics.

## Setup

1. Copy `.env.example` to `.env` and fill in values.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

## Admin usage

1. Send `/admin` from the bot owner account (or a delegated admin with **Manage subscriptions** permission).
2. Open **Subscriptions CRM** to:
   - Add customers (phone, username, password, plan, dates, optional Telegram ID for reminders)
   - Search by phone or service username
   - Edit, renew, or delete records
   - View expiring/expired lists and statistics
   - Configure renewal offer text and reminder days (e.g. `3,1` = 3 days and 1 day before expiry)

## Reminders

Daily jobs run at each hour in `REMINDER_CHECK_HOURS` (default `9,21` = 9:00 and 21:00) in `TIMEZONE`. Customers with a linked Telegram user ID receive a reminder when their subscription is N days from ending (N from bot settings). Staff copies and the daily summary are posted to the Telegram channel set in `REMINDERS_CHANNEL_ID` (add the bot as an admin in that channel).

## Data

SQLite database path is set via `DB_PATH`. Back up the `data/` folder before updates.

## Security

Service passwords are stored in the database as plain text (same as sibling bots in this project). Restrict access to the server and database file.
