import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from start import start_command, admin_command
from common.common import create_folders
from common.back_to_home_page import (
    back_to_admin_home_page_handler,
    back_to_user_home_page_handler,
)
from common.error_handler import error_handler
from common.force_join import check_joined_handler

from user.user_calls import *
from user.user_settings import *

from admin.admin_calls import *
from admin.admin_settings import *
from admin.broadcast import *
from admin.ban import *
from admin.force_join_chats_settings import *
from admin.manage_users_settings import *
from admin.subscriptions import *

from models import init_db
from Config import Config
from jobs.subscription_reminders import check_expiring_subscriptions

from MyApp import MyApp


def setup_and_run():
    create_folders()
    init_db()

    app = MyApp.build_app()

    app.add_handler(user_settings_handler)
    app.add_handler(change_lang_handler)

    # ADMIN SETTINGS
    app.add_handler(show_admins_handler)
    app.add_handler(add_admin_handler)
    app.add_handler(remove_admin_handler)
    app.add_handler(edit_admin_permissions_handler)
    app.add_handler(admin_settings_handler)

    # MANAGE USERS SETTINGS
    app.add_handler(manage_users_settings_handler)
    app.add_handler(export_users_handler)

    # FORCE JOIN CHATS
    app.add_handler(add_force_join_chat_handler)
    app.add_handler(remove_force_join_chat_handler)
    app.add_handler(show_force_join_chats_handler)
    app.add_handler(force_join_chats_settings_handler)

    app.add_handler(broadcast_message_handler)

    app.add_handler(check_joined_handler)

    app.add_handler(ban_unban_user_handler)

    # SUBSCRIPTIONS CRM
    app.add_handler(add_customer_handler)
    app.add_handler(search_customer_handler)
    app.add_handler(edit_customer_handler)
    app.add_handler(offer_settings_handler)
    app.add_handler(subs_stats_handler)
    app.add_handler(subs_expiring_handler)
    app.add_handler(subs_expired_handler)
    app.add_handler(subs_view_handler)
    app.add_handler(subs_renew_handler)
    app.add_handler(subs_delete_prompt_handler)
    app.add_handler(subscriptions_crm_handler)

    app.add_handler(admin_command)
    app.add_handler(start_command)
    app.add_handler(find_id_handler)
    app.add_handler(hide_ids_keyboard_handler)
    app.add_handler(back_to_user_home_page_handler)
    app.add_handler(back_to_admin_home_page_handler)

    app.add_error_handler(error_handler)

    # app.job_queue.run_daily(
    #     callback=check_expiring_subscriptions,
    #     time=datetime.time(
    #         Config.REMINDER_CHECK_HOUR, 0, tzinfo=ZoneInfo(Config.TIMEZONE)
    #     ),
    #     name="subscription_expiry_reminders",
    #     job_kwargs={
    #         "id": "subscription_expiry_reminders",
    #         "misfire_grace_time": None,
    #         "coalesce": True,
    #         "replace_existing": True,
    #     },
    # )
    app.job_queue.run_once(
        callback=check_expiring_subscriptions,
        when=10,
    )

    app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
