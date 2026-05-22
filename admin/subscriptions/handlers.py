import logging
import os
import tempfile
from datetime import date, datetime, timedelta

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from custom_filters import PrivateChatAndAdmin, PermissionFilter
from common.lang_dicts import TEXTS, get_lang
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_admin_keyboard,
)
from common.back_to_home_page import back_to_admin_home_page_handler
from common.subscription_utils import (
    normalize_phone,
    parse_date,
    format_date,
    compute_end_date,
)
from jobs.subscription_reminders import check_expiring_subscriptions
from admin.subscriptions.keyboards import (
    build_confirm_add_button,
    build_delete_confirm_button,
    build_subscriptions_main_keyboard,
    build_duration_keyboard,
    build_start_date_keyboard,
    build_confirm_dates_keyboard,
    build_search_method_keyboard,
    build_customer_actions_keyboard,
    build_customer_pick_keyboard,
    build_edit_fields_keyboard,
    build_list_keyboard,
    build_offer_settings_keyboard,
)
from admin.subscriptions.excel_io import (
    export_customers_workbook,
    import_customers_workbook,
    safe_unlink,
)
from admin.subscriptions.functions import (
    format_customer_card,
    get_stats,
    search_by_phone,
    search_by_username,
    get_expiring_customers,
    get_expired_customers,
    clear_reminders_for_customer,
    preview_customer_card,
)
from models.BotSettings import (
    SETTING_RENEWAL_OFFER,
    SETTING_REMINDER_DAYS,
    SETTING_REMINDER_TEMPLATE,
)
from start import admin_command, start_command
import models

logger = logging.getLogger(__name__)

(
    ADD_NAME,
    ADD_PHONE,
    ADD_USERNAME,
    ADD_PASSWORD,
    ADD_TYPE,
    ADD_DURATION,
    ADD_DURATION_CUSTOM,
    ADD_START,
    ADD_START_CUSTOM,
    ADD_CONFIRM_DATES,
    ADD_END_OVERRIDE,
    ADD_NOTES,
    ADD_TELEGRAM,
    ADD_CONFIRM,
) = range(14)

EDIT_FIELD, EDIT_VALUE = range(2)
OFFER_OPTION, OFFER_TEXT, REMINDER_TEMPLATE, REMINDER_DAYS = range(4)
DELETE_CONFIRM = 0
DURATION_CHOICE, CUSTOM_DURATION = range(2)
SEARCH_METHOD, SEARCH_INPUT, CUSTOMER_PICK = range(3)
IMPORT_FILE = 0


def _allowed(update: Update) -> bool:
    return PrivateChatAndAdmin().filter(update) and PermissionFilter(
        models.Permission.MANAGE_SUBSCRIPTIONS
    ).filter(update)


def _draft(context) -> dict:
    if "subs_draft" not in context.user_data:
        context.user_data["subs_draft"] = {}
    return context.user_data["subs_draft"]


async def subscriptions_crm_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subscriptions_crm_title"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


async def subs_run_reminders_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    await update.callback_query.answer(
        text=TEXTS[lang]["subs_reminders_running"],
    )
    sent_to_customers, sent_to_channel, failed = await check_expiring_subscriptions(
        context
    )
    if sent_to_customers or sent_to_channel or failed:
        result = TEXTS[lang]["subs_reminder_summary"].format(
            sent_to_customers=sent_to_customers,
            sent_to_channel=sent_to_channel,
            failed=failed,
        )
    else:
        result = TEXTS[lang]["subs_reminders_run_none"]
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subscriptions_crm_title"] + "\n\n" + result,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


async def subs_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    with models.session_scope() as s:
        stats = get_stats(s)
    text = TEXTS[lang]["subs_stats_text"].format(**stats)
    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            build_back_to_home_page_button(lang=lang, is_admin=True)
        ),
    )
    return ConversationHandler.END


async def subs_expiring_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    page = int(update.callback_query.data.split("_")[-1])
    with models.session_scope() as s:
        items, total = get_expiring_customers(s, page)
    if not items:
        await update.callback_query.answer(
            text=TEXTS[lang]["subs_no_customers_in_list"],
            show_alert=True,
        )
        return ConversationHandler.END
    keyboard = build_list_keyboard(items, "expiring", page, total)
    keyboard.append(build_back_button("subscriptions_crm", lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_expiring_list_title"].format(count=total),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


async def subs_expired_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    page = int(update.callback_query.data.split("_")[-1])
    with models.session_scope() as s:
        items, total = get_expired_customers(s, page)
    if not items:
        await update.callback_query.answer(
            text=TEXTS[lang]["subs_no_customers_in_list"],
            show_alert=True,
        )
        return ConversationHandler.END
    keyboard = build_list_keyboard(items, "expired", page, total)
    keyboard.append(build_back_button("subscriptions_crm", lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_expired_list_title"].format(count=total),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Add customer ---
async def subs_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    context.user_data["subs_draft"] = {}
    back_buttons = [
        build_back_button(data="subscriptions_crm", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_add_instruction"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_NAME


async def subs_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    back_buttons = [
        build_back_button(data="back_to_subs_add_name", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.message:
        draft["name"] = update.message.text.strip() or None
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_phone"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_PHONE
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_phone"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_PHONE


back_to_subs_add_name = subs_add_start


async def subs_add_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_add_phone", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.message:
        phone = normalize_phone(update.message.text)
        if len(phone) < 8:
            await update.message.reply_text(TEXTS[lang]["subs_invalid_phone"])
            return ADD_PHONE
        _draft(context)["phone"] = phone
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_username"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_USERNAME
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_username"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_USERNAME


back_to_subs_add_phone = subs_add_name


async def subs_add_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_add_username", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.message:
        _draft(context)["service_username"] = update.message.text.strip().lstrip("@")
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_password"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_PASSWORD
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_password"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_PASSWORD


back_to_subs_add_username = subs_add_phone


async def subs_add_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_add_password", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.message:
        _draft(context)["service_password"] = update.message.text.strip()
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_subscription_type"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_TYPE
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_subscription_type"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_TYPE


back_to_subs_add_password = subs_add_username


async def subs_add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = build_duration_keyboard(lang)
    keyboard.append(build_back_button(data="back_to_subs_add_type", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    if update.message:
        _draft(context)["subscription_type"] = update.message.text.strip()
        await update.message.reply_text(
            text=TEXTS[lang]["subs_choose_duration"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ADD_DURATION
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_choose_duration"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ADD_DURATION


back_to_subs_add_type = subs_add_password


async def subs_add_duration_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    data = update.callback_query.data
    back_buttons = [
        build_back_button(data="back_to_subs_add_duration_cb", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if data in ["subs_dur_custom", "back_to_subs_add_duration_custom"]:
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_enter_custom_duration"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_DURATION_CUSTOM
    elif not data.startswith("back"):
        days = int(data.split("_")[-1])
        _draft(context)["duration_days"] = days
    keyboard = build_start_date_keyboard(lang)
    keyboard.extend(back_buttons)
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_choose_start_date"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ADD_START


back_to_subs_add_duration_cb = subs_add_type


async def subs_add_duration_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = build_start_date_keyboard(lang)
    keyboard.append(
        build_back_button(data="back_to_subs_add_duration_custom", lang=lang)
    )
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    if update.message:
        try:
            days = int(update.message.text.strip())
            if days < 1:
                raise ValueError
        except ValueError:
            await update.message.reply_text(TEXTS[lang]["subs_invalid_duration"])
            return ADD_DURATION_CUSTOM
        _draft(context)["duration_days"] = days
        await update.message.reply_text(
            text=TEXTS[lang]["subs_choose_start_date"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_choose_start_date"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return ADD_START


back_to_subs_add_duration_custom = subs_add_duration_cb


async def subs_add_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    back_buttons = [
        build_back_button(data="back_to_subs_add_start_cb", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.callback_query.data == "subs_start_today":
        keyboard = build_confirm_dates_keyboard(lang)
        keyboard.extend(back_buttons)
        draft["start_date"] = date.today()
        end = compute_end_date(draft["start_date"], draft["duration_days"])
        draft["end_date"] = end
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_confirm_dates"].format(
                start=format_date(draft["start_date"]),
                end=format_date(end),
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ADD_CONFIRM_DATES
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_start_date"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_START_CUSTOM


back_to_subs_add_start_cb = subs_add_duration_custom


async def subs_add_start_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = build_confirm_dates_keyboard(lang)
    keyboard.append(build_back_button(data="back_to_subs_add_start_custom", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    draft = _draft(context)
    if update.message:
        start = parse_date(update.message.text)
        if not start:
            await update.message.reply_text(TEXTS[lang]["subs_invalid_date"])
            return ADD_START_CUSTOM
        draft["start_date"] = start
        draft["end_date"] = compute_end_date(start, draft["duration_days"])
        await update.message.reply_text(
            text=TEXTS[lang]["subs_confirm_dates"].format(
                start=format_date(draft["start_date"]),
                end=format_date(draft["end_date"]),
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_confirm_dates"].format(
                start=format_date(draft["start_date"]),
                end=format_date(draft["end_date"]),
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return ADD_CONFIRM_DATES


back_to_subs_add_start_custom = subs_add_start_cb


async def subs_add_dates_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_add_dates_cb", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.callback_query.data == "subs_dates_edit_end":
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_enter_end_date"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_END_OVERRIDE
    draft = _draft(context)
    draft["end_date_override"] = False
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_notes"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_NOTES


back_to_subs_add_dates_cb = subs_add_start_custom


async def subs_add_end_override(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    back_buttons = [
        build_back_button(data="back_to_subs_add_end_override", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if update.message:
        end = parse_date(update.message.text)
        if not end:
            await update.message.reply_text(TEXTS[lang]["subs_invalid_date"])
            return ADD_END_OVERRIDE
        draft["end_date"] = end
        draft["duration_days"] = (end - draft["start_date"]).days
        draft["end_date_override"] = True
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_notes"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
    else:
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_enter_notes"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
    return ADD_NOTES


back_to_subs_add_end_override = subs_add_dates_cb


async def subs_add_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    back_buttons = []
    if draft["end_date_override"]:
        back_buttons.append(
            build_back_button(data="back_to_subs_add_notes_end_override", lang=lang)
        )
    else:
        back_buttons.append(build_back_button(data="back_to_subs_add_notes", lang=lang))
    back_buttons.append(build_back_to_home_page_button(lang=lang)[0])
    if update.message:
        draft["notes"] = update.message.text.strip() or None
        await update.message.reply_text(
            text=TEXTS[lang]["subs_enter_telegram_id"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADD_TELEGRAM
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_enter_telegram_id"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return ADD_TELEGRAM


back_to_subs_add_notes = subs_add_dates_cb
back_to_subs_add_notes_end_override = subs_add_end_override


async def subs_add_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    keyboard = build_confirm_add_button(lang)
    keyboard.append(build_back_button(data="back_to_subs_add_telegram", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    if update.message:
        text = update.message.text.strip()
        try:
            draft["telegram_user_id"] = int(text)
        except ValueError:
            await update.message.reply_text(TEXTS[lang]["subs_invalid_telegram_id"])
            return ADD_TELEGRAM
        card = preview_customer_card(draft, lang)
        await update.message.reply_text(
            text=TEXTS[lang]["subs_confirm_add"].format(card=card),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        card = preview_customer_card(draft, lang)
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_confirm_add"].format(card=card),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return ADD_CONFIRM


back_to_subs_add_telegram = subs_add_notes


async def subs_add_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    draft = _draft(context)
    customer = models.Customer(
        name=draft.get("name"),
        phone=draft["phone"],
        service_username=draft["service_username"],
        service_password=draft["service_password"],
        subscription_type=draft["subscription_type"],
        duration_days=draft["duration_days"],
        start_date=draft["start_date"],
        end_date=draft["end_date"],
        notes=draft.get("notes"),
        telegram_user_id=draft.get("telegram_user_id"),
    )
    with models.session_scope() as s:
        s.add(customer)
    context.user_data.pop("subs_draft", None)
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_customer_added"],
        reply_markup=build_admin_keyboard(lang=lang, user_id=update.effective_user.id),
    )
    return ConversationHandler.END


# --- Search ---
async def subs_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = build_search_method_keyboard(lang)
    keyboard.append(build_back_button(data="subscriptions_crm", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_search_choose"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return SEARCH_METHOD


async def subs_search_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_search_method", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    if not update.callback_query.data.startswith("back"):
        search_mode = update.callback_query.data.replace("subs_search_", "")
        context.user_data["subs_search_mode"] = search_mode
    else:
        search_mode = context.user_data["subs_search_mode"]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang][f"subs_search_enter_{search_mode}"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return SEARCH_INPUT


back_to_subs_search_method = subs_search_start


async def subs_search_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    mode = context.user_data.get("subs_search_mode", "phone")
    if update.message:
        search_input = update.message.text
        context.user_data["subs_search_input"] = search_input
    else:
        search_input = context.user_data.get("subs_search_input")
    with models.session_scope() as s:
        if mode == "phone":
            found = search_by_phone(s, search_input)
        else:
            found = search_by_username(s, search_input)
    if not found:
        if update.message:
            await update.message.reply_text(
                text=TEXTS[lang]["subs_customer_not_found"],
            )
            return
    if len(found) == 1:
        card = format_customer_card(found[0], lang)
        keyboard = build_customer_actions_keyboard(lang=lang, customer_id=found[0].id)
        keyboard.append(build_back_to_home_page_button(lang=lang)[0])
        if update.message:
            await update.message.reply_text(
                text=card,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await update.callback_query.edit_message_text(
                text=card,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return ConversationHandler.END
    keyboard = build_customer_pick_keyboard(found, lang)
    keyboard.append(build_back_button(data="back_to_subs_search_input", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    if update.message:
        await update.message.reply_text(
            text=TEXTS[lang]["subs_multiple_found"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_multiple_found"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return CUSTOMER_PICK


back_to_subs_search_input = subs_search_method


async def subs_view_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = int(update.callback_query.data.split("_")[-1])
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
    if not customer:
        await update.callback_query.answer(
            TEXTS[lang]["subs_customer_not_found"],
            show_alert=True,
        )
        return ConversationHandler.END
    keyboard = build_customer_actions_keyboard(lang, customer_id)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=format_customer_card(customer, lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Renew ---
async def subs_renew_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    if not update.callback_query.data.startswith("back"):
        customer_id = int(update.callback_query.data.split("_")[-1])
        context.user_data["subs_renew_id"] = customer_id
    else:
        customer_id = context.user_data["subs_renew_id"]
    keyboard = build_duration_keyboard(
        lang, prefix="subs_renew_dur", customer_id=customer_id
    )
    keyboard.append(build_back_button(data="back_to_subs_renew_start", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_renew_choose_duration"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return DURATION_CHOICE


back_to_subs_renew_start = subs_search_input


async def subs_renew_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    parts = update.callback_query.data.split("_")
    customer_id = int(parts[3])
    if parts[-1] == "custom":
        back_buttons = [
            build_back_button(data="back_to_subs_renew_apply", lang=lang),
            build_back_to_home_page_button(lang=lang)[0],
        ]
        context.user_data["subs_renew_id"] = customer_id
        context.user_data["subs_renew_custom"] = True
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["subs_enter_custom_duration"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return CUSTOM_DURATION
    days = int(parts[4])
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
        if customer:
            customer.renew(days)
            clear_reminders_for_customer(s, customer_id)
            end = format_date(customer.end_date)
        else:
            await update.callback_query.answer(
                TEXTS[lang]["subs_customer_not_found"],
                show_alert=True,
            )
            return
    keyboard = build_customer_actions_keyboard(lang=lang, customer_id=customer_id)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_renew_success"].format(end_date=end),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


back_to_subs_renew_apply = subs_renew_start


async def subs_renew_custom_duration(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update) or not context.user_data.get("subs_renew_custom"):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = context.user_data.get("subs_renew_id")
    try:
        days = int(update.message.text.strip())
        if days < 1:
            raise ValueError
    except ValueError:
        await update.message.reply_text(TEXTS[lang]["subs_invalid_duration"])
        return
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
        if customer:
            customer.renew(days)
            clear_reminders_for_customer(s, customer_id)
            end = format_date(customer.end_date)
    context.user_data.pop("subs_renew_custom", None)
    context.user_data.pop("subs_renew_id", None)
    keyboard = build_customer_actions_keyboard(lang=lang, customer_id=customer_id)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.message.reply_text(
        text=TEXTS[lang]["subs_renew_success"].format(end_date=end),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Delete ---
async def subs_delete_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = int(update.callback_query.data.split("_")[-1])
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
    if not customer:
        await update.callback_query.answer(
            TEXTS[lang]["subs_customer_not_found"],
            show_alert=True,
        )
        return
    keyboard = build_delete_confirm_button(lang, customer_id)
    keyboard.append(build_back_button(data="back_to_subs_delete_prompt", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_delete_confirm"].format(
            card=format_customer_card(customer, lang)
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return DELETE_CONFIRM


back_to_subs_delete_prompt = subs_search_input


async def subs_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = int(update.callback_query.data.split("_")[-1])
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
        if customer:
            s.delete(customer)
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_customer_deleted"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Edit ---
async def subs_edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = int(update.callback_query.data.split("_")[-1])
    keyboard = build_edit_fields_keyboard(lang=lang, customer_id=customer_id)
    keyboard.append(build_back_button(data="back_to_subs_edit_menu", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_edit_choose_field"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return EDIT_FIELD


back_to_subs_edit_menu = subs_search_input


async def subs_edit_field_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    parts = update.callback_query.data.split("_")
    customer_id = int(parts[2])
    field = "_".join(parts[3:])
    context.user_data["subs_edit_id"] = customer_id
    context.user_data["subs_edit_field"] = field
    back_buttons = [
        build_back_button(data="back_to_subs_edit_field_pick", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_edit_enter_value"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return EDIT_VALUE


back_to_subs_edit_field_pick = subs_edit_menu


async def subs_edit_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    customer_id = context.user_data.get("subs_edit_id")
    field = context.user_data.get("subs_edit_field")
    value = update.message.text.strip()
    with models.session_scope() as s:
        customer = s.get(models.Customer, customer_id)
        if field == "phone":
            phone = normalize_phone(value)
            if len(phone) < 8:
                await update.message.reply_text(TEXTS[lang]["subs_invalid_phone"])
                return
            customer.phone = phone
        elif field == "service_username":
            customer.service_username = value.lstrip("@")
        elif field == "service_password":
            customer.service_password = value
        elif field == "subscription_type":
            customer.subscription_type = value
        elif field == "duration_days":
            try:
                days = int(value)
                if days < 1:
                    raise ValueError
                customer.duration_days = days
                customer.end_date = customer.start_date + timedelta(days=days)
            except ValueError:
                await update.message.reply_text(TEXTS[lang]["subs_invalid_duration"])
                return
        elif field == "end_date":
            end = parse_date(value)
            if not end:
                await update.message.reply_text(TEXTS[lang]["subs_invalid_date"])
                return
            customer.end_date = end
            customer.duration_days = (end - customer.start_date).days
        elif field == "notes":
            customer.notes = value or None
        elif field == "telegram_user_id":
            if value.lower() in ("-", "none", "حذف", "delete"):
                customer.telegram_user_id = None
            else:
                try:
                    customer.telegram_user_id = int(value)
                except ValueError:
                    await update.message.reply_text(
                        TEXTS[lang]["subs_invalid_telegram_id"]
                    )
                    return
        elif field == "name":
            customer.name = value or None
    card = format_customer_card(customer, lang)
    keyboard = build_customer_actions_keyboard(lang=lang, customer_id=customer_id)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.message.reply_text(
        text=TEXTS[lang]["subs_customer_updated"].format(card=card),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Offer settings ---
async def subs_offer_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    with models.session_scope() as s:
        offer = models.BotSettings.get(s, SETTING_RENEWAL_OFFER, "")
        template = models.BotSettings.get(s, SETTING_REMINDER_TEMPLATE, "")
        days = models.BotSettings.get(s, SETTING_REMINDER_DAYS, "3")
    text = (
        TEXTS[lang]["subs_offer_settings_title"]
        + "\n\n"
        + TEXTS[lang]["subs_current_offer"].format(text=offer)
        + "\n\n"
        + TEXTS[lang]["subs_current_reminder_template"].format(text=template[:500])
        + "\n\n"
        + TEXTS[lang]["subs_current_reminder_days"].format(days=days)
    )
    keyboard = build_offer_settings_keyboard(lang)
    keyboard.append(build_back_button(data="subscriptions_crm", lang=lang))
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return OFFER_OPTION


async def subs_edit_offer_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_edit_offer_start", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_edit_offer_text"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return OFFER_TEXT


back_to_subs_edit_offer_start = subs_offer_settings


async def subs_edit_offer_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    with models.session_scope() as s:
        models.BotSettings.set(s, SETTING_RENEWAL_OFFER, update.message.text)
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.message.reply_text(
        text=TEXTS[lang]["subs_edit_offer_saved"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


async def subs_edit_reminder_template_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_edit_reminder_template_start", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_edit_reminder_template"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return REMINDER_TEMPLATE


back_to_subs_edit_reminder_template_start = subs_offer_settings


async def subs_edit_reminder_template_save(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    with models.session_scope() as s:
        models.BotSettings.set(s, SETTING_REMINDER_TEMPLATE, update.message.text)
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.message.reply_text(
        text=TEXTS[lang]["subs_edit_reminder_template_saved"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


async def subs_edit_reminder_days_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    back_buttons = [
        build_back_button(data="back_to_subs_edit_reminder_days_start", lang=lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_edit_reminder_days"],
        reply_markup=InlineKeyboardMarkup(back_buttons),
    )
    return REMINDER_DAYS


back_to_subs_edit_reminder_days_start = subs_offer_settings


async def subs_edit_reminder_days_save(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    from common.subscription_utils import parse_reminder_days

    days = parse_reminder_days(update.message.text)
    if not days:
        await update.message.reply_text(TEXTS[lang]["subs_invalid_duration"])
        return REMINDER_DAYS
    with models.session_scope() as s:
        models.BotSettings.set(s, SETTING_REMINDER_DAYS, ",".join(str(d) for d in days))
    keyboard = build_subscriptions_main_keyboard(lang)
    keyboard.append(build_back_to_home_page_button(lang=lang)[0])
    await update.message.reply_text(
        text=TEXTS[lang]["subs_edit_reminder_days_saved"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


# --- Excel import/export ---
async def subs_export_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    await update.callback_query.answer(
        text=TEXTS[lang]["subs_exporting_customers"],
        show_alert=True,
    )
    await update.callback_query.delete_message()

    excel_path = None
    try:
        with models.session_scope() as s:
            excel_path = export_customers_workbook(lang, s)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"customers_export_{timestamp}.xlsx"
        with open(excel_path, "rb") as excel_file:
            await context.bot.send_document(
                chat_id=update.effective_user.id,
                document=excel_file,
                filename=filename,
            )
        text = TEXTS[lang]["subs_customers_exported_success"]
    except Exception:
        logger.exception("Customer export failed")
        text = TEXTS[lang]["export_error"]
    finally:
        safe_unlink(excel_path)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text + "\n\n" + TEXTS[lang]["continue_with_admin_command"],
    )
    return ConversationHandler.END


async def subs_import_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    keyboard = [
        build_back_button("subscriptions_crm", lang),
        build_back_to_home_page_button(lang=lang)[0],
    ]
    await update.callback_query.edit_message_text(
        text=TEXTS[lang]["subs_import_instruction"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return IMPORT_FILE


async def subs_import_invalid_file(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(TEXTS[lang]["subs_import_invalid_file"])
    return IMPORT_FILE


async def subs_import_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _allowed(update):
        return ConversationHandler.END
    lang = get_lang(update.effective_user.id)
    doc = update.message.document
    if not doc or not (doc.file_name or "").lower().endswith(".xlsx"):
        await update.message.reply_text(TEXTS[lang]["subs_import_invalid_file"])
        return IMPORT_FILE

    await update.message.reply_text(TEXTS[lang]["subs_importing_customers"])
    excel_path = None
    try:
        tg_file = await context.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            excel_path = tmp.name
        await tg_file.download_to_drive(excel_path)
        with models.session_scope() as s:
            result = import_customers_workbook(excel_path, lang, s)
    except Exception:
        logger.exception("Customer import failed")
        await update.message.reply_text(TEXTS[lang]["export_error"])
        safe_unlink(excel_path)
        return ConversationHandler.END
    finally:
        safe_unlink(excel_path)

    summary = TEXTS[lang]["subs_import_result"].format(
        created=result.created,
        updated=result.updated,
        skipped=result.skipped,
        error_count=len(result.errors),
    )
    if result.errors:
        lines = "\n".join(f"{e.row}: {e.message}" for e in result.errors[:10])
        if len(result.errors) > 10:
            lines += f"\n… (+{len(result.errors) - 10})"
        summary += "\n\n" + TEXTS[lang]["subs_import_errors_sample"].format(
            lines=lines
        )
    elif not result.created and not result.updated:
        summary = TEXTS[lang]["subs_import_nothing_done"]

    await update.message.reply_text(
        summary,
        reply_markup=build_admin_keyboard(
            lang=lang, user_id=update.effective_user.id
        ),
    )
    return ConversationHandler.END


# --- Handler registration ---
subscriptions_crm_handler = CallbackQueryHandler(
    callback=subscriptions_crm_menu,
    pattern=r"^subscriptions_crm$",
)

subs_run_reminders_now_handler = CallbackQueryHandler(
    callback=subs_run_reminders_now,
    pattern=r"^subs_run_reminders_now$",
)

subs_stats_handler = CallbackQueryHandler(
    callback=subs_stats,
    pattern=r"^subs_stats$",
)

subs_expiring_handler = CallbackQueryHandler(
    callback=subs_expiring_list,
    pattern=r"^subs_expiring_\d+$",
)

subs_expired_handler = CallbackQueryHandler(
    callback=subs_expired_list,
    pattern=r"^subs_expired_\d+$",
)

subs_view_handler = CallbackQueryHandler(
    callback=subs_view_customer,
    pattern=r"^subs_view_\d+$",
)

subs_export_excel_handler = CallbackQueryHandler(
    callback=subs_export_excel,
    pattern=r"^subs_export_excel$",
)

import_customer_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_import_start,
            pattern=r"^subs_import_excel$",
        )
    ],
    states={
        IMPORT_FILE: [
            MessageHandler(
                filters.Document.FileExtension("xlsx"),
                callback=subs_import_file,
            ),
            MessageHandler(
                filters.ALL & ~filters.COMMAND,
                callback=subs_import_invalid_file,
            ),
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(
            callback=subscriptions_crm_menu,
            pattern=r"^subscriptions_crm$",
        ),
    ],
    name="subs_import_excel",
    persistent=True,
)

add_customer_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_add_start,
            pattern=r"^subs_add_customer$",
        )
    ],
    states={
        ADD_NAME: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_add_name,
            ),
        ],
        ADD_PHONE: [
            MessageHandler(
                filters=filters.Regex(r"^\+?\d+$"),
                callback=subs_add_phone,
            )
        ],
        ADD_USERNAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback=subs_add_username,
            )
        ],
        ADD_PASSWORD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback=subs_add_password,
            )
        ],
        ADD_TYPE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback=subs_add_type,
            )
        ],
        ADD_DURATION: [
            CallbackQueryHandler(
                callback=subs_add_duration_cb,
                pattern=r"^subs_dur_",
            )
        ],
        ADD_DURATION_CUSTOM: [
            MessageHandler(
                filters=filters.Regex(r"^\d+$"),
                callback=subs_add_duration_custom,
            )
        ],
        ADD_START: [
            CallbackQueryHandler(
                callback=subs_add_start_cb,
                pattern=r"^subs_start_",
            )
        ],
        ADD_START_CUSTOM: [
            MessageHandler(
                filters=filters.Regex(r"^\d{4}-\d{2}-\d{2}$"),
                callback=subs_add_start_custom,
            )
        ],
        ADD_CONFIRM_DATES: [
            CallbackQueryHandler(
                callback=subs_add_dates_cb,
                pattern=r"^subs_dates_",
            )
        ],
        ADD_END_OVERRIDE: [
            MessageHandler(
                filters=filters.Regex(r"^\d{4}-\d{2}-\d{2}$"),
                callback=subs_add_end_override,
            )
        ],
        ADD_NOTES: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_add_notes,
            ),
        ],
        ADD_TELEGRAM: [
            MessageHandler(
                filters=filters.Regex(r"^-?\d+$"),
                callback=subs_add_telegram,
            ),
        ],
        ADD_CONFIRM: [
            CallbackQueryHandler(
                callback=subs_add_confirm,
                pattern=r"^subs_confirm_save$",
            )
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(
            callback=back_to_subs_add_name, pattern=r"^back_to_subs_add_name$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_phone, pattern=r"^back_to_subs_add_phone$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_username, pattern=r"^back_to_subs_add_username$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_password, pattern=r"^back_to_subs_add_password$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_type, pattern=r"^back_to_subs_add_type$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_duration_cb,
            pattern=r"^back_to_subs_add_duration_cb$",
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_duration_custom,
            pattern=r"^back_to_subs_add_duration_custom$",
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_start_cb, pattern=r"^back_to_subs_add_start_cb$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_start_custom,
            pattern=r"^back_to_subs_add_start_custom$",
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_dates_cb, pattern=r"^back_to_subs_add_dates_cb$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_end_override,
            pattern=r"^back_to_subs_add_end_override$",
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_notes_end_override,
            pattern=r"^back_to_subs_add_notes_end_override$",
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_notes, pattern=r"^back_to_subs_add_notes$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_add_telegram, pattern=r"^back_to_subs_add_telegram$"
        ),
    ],
    name="subs_add_customer",
    persistent=True,
)

search_customer_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_search_start,
            pattern=r"^subs_search$",
        )
    ],
    states={
        SEARCH_METHOD: [
            CallbackQueryHandler(
                callback=subs_search_method,
                pattern=r"^subs_search_",
            ),
        ],
        SEARCH_INPUT: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_search_input,
            ),
        ],
        CUSTOMER_PICK: [
            CallbackQueryHandler(
                callback=subs_view_customer,
                pattern=r"^subs_pick_\d+$",
            )
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(
            callback=back_to_subs_search_method, pattern=r"^back_to_subs_search_method$"
        ),
        CallbackQueryHandler(
            callback=back_to_subs_search_input, pattern=r"^back_to_subs_search_input$"
        ),
    ],
    name="subs_search",
    persistent=True,
)


subs_renew_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_renew_start,
            pattern=r"^subs_renew_\d+$",
        )
    ],
    states={
        DURATION_CHOICE: [
            CallbackQueryHandler(
                callback=subs_renew_apply,
                pattern=r"^subs_renew_dur_\d+_\d+$|^subs_renew_dur_\d+_custom$",
            )
        ],
        CUSTOM_DURATION: [
            MessageHandler(
                filters=filters.Regex(r"^\d+$"),
                callback=subs_renew_custom_duration,
            )
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(back_to_subs_renew_start, r"^back_to_subs_renew_start$"),
        CallbackQueryHandler(back_to_subs_renew_apply, r"^back_to_subs_renew_apply$"),
    ],
    name="subs_renew",
    persistent=True,
)


subs_delete_prompt_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_delete_prompt,
            pattern=r"^subs_delete_\d+$",
        )
    ],
    states={
        DELETE_CONFIRM: [
            CallbackQueryHandler(
                callback=subs_delete_confirm,
                pattern=r"^subs_delete_confirm_\d+$",
            )
        ]
    },
    fallbacks=[
        admin_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(
            back_to_subs_delete_prompt, r"^back_to_subs_delete_prompt$"
        ),
    ],
    name="subs_delete",
    persistent=True,
)


edit_customer_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_edit_menu,
            pattern=r"^subs_edit_\d+$",
        )
    ],
    states={
        EDIT_FIELD: [
            CallbackQueryHandler(
                callback=subs_edit_field_pick,
                pattern=r"^subs_ef_",
            )
        ],
        EDIT_VALUE: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_edit_save,
            )
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(back_to_subs_edit_menu, r"^back_to_subs_edit_menu$"),
        CallbackQueryHandler(
            back_to_subs_edit_field_pick, r"^back_to_subs_edit_field_pick$"
        ),
    ],
    name="subs_edit",
    persistent=True,
)


offer_settings_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=subs_offer_settings,
            pattern=r"^subs_offer_settings$",
        ),
    ],
    states={
        OFFER_OPTION: [
            CallbackQueryHandler(
                callback=subs_edit_offer_start,
                pattern=r"^subs_edit_offer_text$",
            ),
            CallbackQueryHandler(
                callback=subs_edit_reminder_template_start,
                pattern=r"^subs_edit_reminder_template$",
            ),
            CallbackQueryHandler(
                callback=subs_edit_reminder_days_start,
                pattern=r"^subs_edit_reminder_days$",
            ),
        ],
        OFFER_TEXT: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_edit_offer_save,
            )
        ],
        REMINDER_TEMPLATE: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_edit_reminder_template_save,
            )
        ],
        REMINDER_DAYS: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=subs_edit_reminder_days_save,
            )
        ],
    },
    fallbacks=[
        admin_command,
        start_command,
        back_to_admin_home_page_handler,
        subscriptions_crm_handler,
        CallbackQueryHandler(
            back_to_subs_edit_offer_start, r"^back_to_subs_edit_offer_start$"
        ),
        CallbackQueryHandler(
            back_to_subs_edit_reminder_template_start,
            r"^back_to_subs_edit_reminder_template_start$",
        ),
        CallbackQueryHandler(
            back_to_subs_edit_reminder_days_start,
            r"^back_to_subs_edit_reminder_days_start$",
        ),
    ],
    name="subs_offer_settings",
    persistent=True,
)
