from notifications.telegram import TelegramNotifier

_notifier = TelegramNotifier()


def get_notifier() -> TelegramNotifier:
    return _notifier
