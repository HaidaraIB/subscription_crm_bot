from telegram import InlineKeyboardButton
from common.lang_dicts import BUTTONS
import models

DURATION_PRESETS = [
    ("subs_duration_7", 7, "subs_dur_7"),
    ("subs_duration_30", 30, "subs_dur_30"),
    ("subs_duration_90", 90, "subs_dur_90"),
    ("subs_duration_365", 365, "subs_dur_365"),
]


def build_subscriptions_main_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_add_customer"],
                callback_data="subs_add_customer",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_search"],
                callback_data="subs_search",
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_expiring"],
                callback_data="subs_expiring_0",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_expired"],
                callback_data="subs_expired_0",
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_stats"],
                callback_data="subs_stats",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_offer_settings"],
                callback_data="subs_offer_settings",
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_run_reminders_now"],
                callback_data="subs_run_reminders_now",
            ),
        ],
    ]
    return keyboard


def build_duration_keyboard(
    lang: models.Language,
    prefix: str = "subs_dur",
    customer_id: int | None = None,
):
    keyboard = []
    row = []
    for btn_key, days, _cb in DURATION_PRESETS:
        if customer_id is not None:
            cb_data = f"{prefix}_{customer_id}_{days}"
        else:
            cb_data = f"{prefix}_{days}"
        row.append(
            InlineKeyboardButton(
                BUTTONS[lang][btn_key],
                callback_data=cb_data,
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    custom_cb = (
        f"{prefix}_{customer_id}_custom"
        if customer_id is not None
        else f"{prefix}_custom"
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_duration_custom"],
                callback_data=custom_cb,
            )
        ]
    )
    return keyboard


def build_start_date_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_start_today"],
                callback_data="subs_start_today",
            )
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_start_custom"],
                callback_data="subs_start_custom",
            )
        ],
    ]
    return keyboard


def build_confirm_dates_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["confirm_button"],
                callback_data="subs_dates_confirm",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_edit_end_date"],
                callback_data="subs_dates_edit_end",
            ),
        ],
    ]
    return keyboard



def build_confirm_add_button(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["confirm_button"],
                callback_data="subs_confirm_save",
            )
        ],
    ]
    return keyboard


def build_search_method_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_search_by_phone"],
                callback_data="subs_search_phone",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_search_by_username"],
                callback_data="subs_search_username",
            ),
        ],
    ]
    return keyboard


def build_customer_actions_keyboard(lang: models.Language, customer_id: int):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_edit"],
                callback_data=f"subs_edit_{customer_id}",
            ),
            InlineKeyboardButton(
                BUTTONS[lang]["subs_renew"],
                callback_data=f"subs_renew_{customer_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_delete"],
                callback_data=f"subs_delete_{customer_id}",
            )
        ],
    ]
    return keyboard


def build_customer_pick_keyboard(
    customers: list[models.Customer],
    lang: models.Language,
    prefix: str = "subs_pick",
):
    keyboard = []
    for c in customers[:15]:
        label = f"{c.name} ({c.phone})"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=label,
                    callback_data=f"{prefix}_{c.id}",
                )
            ]
        )
    return keyboard


def build_edit_fields_keyboard(lang: models.Language, customer_id: int):
    fields = [
        ("subs_edit_name", "name"),
        ("subs_edit_phone", "phone"),
        ("subs_edit_username", "service_username"),
        ("subs_edit_password", "service_password"),
        ("subs_edit_type", "subscription_type"),
        ("subs_edit_duration", "duration_days"),
        ("subs_edit_end_date_field", "end_date"),
        ("subs_edit_notes", "notes"),
        ("subs_edit_telegram", "telegram_user_id"),
    ]
    keyboard = []
    row = []
    for btn_key, field in fields:
        row.append(
            InlineKeyboardButton(
                BUTTONS[lang][btn_key],
                callback_data=f"subs_ef_{customer_id}_{field}",
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return keyboard


def build_delete_confirm_button(lang: models.Language, customer_id: int):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["confirm_button"],
                callback_data=f"subs_delete_confirm_{customer_id}",
            )
        ],
    ]
    return keyboard


def build_list_keyboard(
    customers: list,
    lang: models.Language,
    list_type: str,
    page: int,
    total: int,
):
    keyboard = []
    for c in customers:
        status = "✅" if c.is_active() else "❌"
        label = f"{status} #{c.id} {c.service_username} → {c.end_date}"
        keyboard.append(
            [InlineKeyboardButton(label[:60], callback_data=f"subs_view_{c.id}")]
        )
    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton("◀️", callback_data=f"subs_{list_type}_{page - 1}")
        )
    if (page + 1) * 10 < total:
        nav.append(
            InlineKeyboardButton("▶️", callback_data=f"subs_{list_type}_{page + 1}")
        )
    if nav:
        keyboard.append(nav)
    return keyboard


def build_offer_settings_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_edit_offer_text_btn"],
                callback_data="subs_edit_offer_text",
            )
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_edit_reminder_template_btn"],
                callback_data="subs_edit_reminder_template",
            )
        ],
        [
            InlineKeyboardButton(
                BUTTONS[lang]["subs_edit_reminder_days_btn"],
                callback_data="subs_edit_reminder_days",
            )
        ],
    ]
    return keyboard
