import models

TEXTS = {
    models.Language.ARABIC: {
        "user_welcome_msg": "أهلاً بك في بوت إدارة الاشتراكات.",
        "admin_welcome_msg": "لوحة إدارة الاشتراكات — استخدم القائمة أدناه.",
        "force_join_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثة البوت أولاً\n\n"
            "<b>اشترك أولاً 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثات البوت أولاً\n\n"
            "<b>اشترك في جميع المحادثات 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "join_first_answer": "قم بالاشتراك بالمحادثة أولاً ❗️",
        "join_all_first_answer": "قم بالاشتراك في جميع المحادثات أولاً ❗️",
        "settings": "الإعدادات ⚙️",
        "change_lang": "اختر اللغة 🌐",
        "change_lang_success": "تم تغيير اللغة بنجاح ✅",
        "home_page": "القائمة الرئيسية 🔝",
        "currently_admin": "تعمل الآن كآدمن 🕹",
        "admin_settings_title": "إعدادات الآدمن 🪄",
        "add_admin_instruction": (
            "اختر حساب الآدمن الذي تريد إضافته بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "admin_added_success": "تمت إضافة الآدمن بنجاح ✅",
        "cannot_remove_owner": "لا يمكنك إزالة مالك البوت من قائمة الآدمنز ❗️",
        "admin_removed_success": "تمت إزالة الآدمن بنجاح ✅",
        "remove_admin_instruction": "اختر من القائمة أدناه الآدمن الذي تريد إزالته.",
        "continue_with_admin_command": "للمتابعة اضغط /admin",
        "keyboard_hidden": "تم الإخفاء ✅",
        "keyboard_shown": "تم الإظهار ✅",
        "ban_instruction": (
            "اختر حساب المستخدم الذي تريد حظره بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "user_not_found": (
            "لم يتم العثور على المستخدم ❌\n"
            "تأكد من الآيدي أو من أن المستخدم قد بدأ محادثة مع البوت من قبل"
        ),
        "user_found": "تم العثور على المستخدم ✅",
        "do_you_want": "هل تريد",
        "operation_success": "تمت العملية بنجاح ✅",
        "ban_confirmation": (
            "معلومات المستخدم:\n"
            "{user_info}\n\n"
            "حالة الحظر الحالية: <b>{ban_status}</b>\n\n"
            "سيتم <b>{action}</b> هذا المستخدم.\n\n"
            "اضغط على زر <b>تأكيد</b> للمتابعة."
        ),
        "user_banned": "محظور 🔒",
        "user_not_banned": "غير محظور 🔓",
        "action_ban": "حظر",
        "action_unban": "فك حظر",
        "send_message": "أرسل الرسالة",
        "send_message_to": "هل تريد إرسال الرسالة إلى",
        "send_user_ids": "قم بإرسال آيديات المستخدمين الذين تريد إرسال الرسالة لهم سطراً سطراً",
        "send_chat_id": "أرسل آيدي القناة/المجموعة",
        "sending_messages": "يقوم البوت بإرسال الرسائل الآن، يمكنك متابعة استخدامه بشكل طبيعي",
        "bot_must_be_member": "يجب أن يكون البوت مشتركاً في هذه القناة/المجموعة حتى يتمكن من النشر فيها",
        "message_published_success": "تم نشر الرسالة في {chat_title} بنجاح ✅",
        "bot_owner": "مالك البوت",
        "force_join_chats_title": "إدارة محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat_instruction": (
            "اختر المحادثة التي تريد إجبار المستخدمين على الانضمام إليها بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "enter_chat_link_instruction": (
            "تم العثور على المحادثة: <b>{chat_title}</b>\n\n"
            "أرسل رابط المحادثة (invite link) أو اسم المستخدم\n\n"
            "مثال: https://t.me/channel_name أو @channel_name"
        ),
        "force_join_chat_added_success": "تمت إضافة محادثة الإجبار على الانضمام بنجاح ✅",
        "force_join_chat_removed_success": "تمت إزالة محادثة الإجبار على الانضمام بنجاح ✅",
        "remove_force_join_chat_instruction": "اختر من القائمة أدناه المحادثة التي تريد إزالتها.",
        "no_force_join_chats": "لا توجد محادثات إجبار على الانضمام حالياً ❗️",
        "force_join_chats_list_title": "قائمة محادثات الإجبار على الانضمام",
        "invalid_chat_id": "آيدي المحادثة غير صحيح ❌",
        "chat_not_found": "لم يتم العثور على المحادثة ❌\nتأكد من الآيدي أو من أن البوت عضو في المحادثة",
        "chat_link_required": "المحادثة لا تحتوي على رابط دعوة. يرجى إرسال رابط الدعوة يدوياً.",
        "invalid_chat_link": "رابط المحادثة غير صحيح ❌\nيجب أن يبدأ بـ https://t.me/ أو @",
        "select_permissions_instruction": "اختر الصلاحيات التي تريد منحها لهذا الآدمن",
        "permissions_selected": "تم اختيار الصلاحيات بنجاح ✅",
        "manage_permissions": "إدارة الصلاحيات 🔐",
        "edit_admin_permissions": "تعديل صلاحيات الآدمن 🔐",
        "select_admin_to_edit_permissions": "اختر الآدمن الذي تريد تعديل صلاحياته",
        "current_permissions": "الصلاحيات الحالية",
        "no_permissions": "لا توجد صلاحيات",
        "permission_granted": "تم منح الصلاحية ✅",
        "permission_revoked": "تم سحب الصلاحية ✅",
        "cannot_edit_owner_permissions": "لا يمكنك تعديل صلاحيات مالك البوت ❗️",
        "permission_ban_users": "حظر/فك حظر المستخدمين",
        "permission_broadcast": "إرسال رسائل جماعية",
        "permission_manage_force_join": "إدارة محادثات الإجبار على الانضمام",
        "permission_view_ids": "عرض معرفات المستخدمين/المحادثات",
        "permission_manage_permissions": "إدارة الصلاحيات",
        "permission_manage_admins": "إدارة الآدمنز",
        "toggle_permission": "تبديل الصلاحية",
        "all_permissions": "جميع الصلاحيات",
        "no_permissions_selected": "لم يتم اختيار أي صلاحيات",
        "no_admins_to_edit": "لا يوجد أدمنز لتعديل صلاحياتهم",
        "you_dont_have_permission_to_manage_permissions": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_manage_admins": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_ban_users": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_broadcast": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_manage_force_join": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_view_ids": "لا يمكنك تعديل صلاحيات الآدمنز",
        "manage_users_settings_title": "إدارة المستخدمين 👥",
        "export_users_to_excel": "تصدير المستخدمين إلى Excel 📊",
        "exporting_users": "جاري تصدير المستخدمين...",
        "users_exported_success": "تم تصدير المستخدمين بنجاح ✅",
        "export_error": "حدث خطأ أثناء التصدير ❌",
        "excel_user_id": "معرف المستخدم",
        "excel_username": "اسم المستخدم",
        "excel_name": "الاسم",
        "excel_language": "اللغة",
        "excel_is_admin": "آدمن",
        "excel_is_banned": "محظور",
        "excel_created_at": "تاريخ الإنشاء",
        "excel_no_username": "غير متوفر",
        "excel_unknown": "غير معروف",
        "excel_yes": "نعم",
        "excel_no": "لا",
        "excel_customer_id": "المعرف",
        "excel_customer_name": "الاسم",
        "excel_phone": "الجوال",
        "excel_service_username": "يوزر الاشتراك",
        "excel_service_password": "كلمة المرور",
        "excel_subscription_type": "نوع الاشتراك",
        "excel_duration_days": "المدة (أيام)",
        "excel_start_date": "تاريخ البداية",
        "excel_end_date": "تاريخ النهاية",
        "excel_telegram_user_id": "آيدي تيليجرام",
        "excel_notes": "ملاحظات",
        "excel_customer_status": "الحالة",
        "lang_arabic": "العربية",
        "lang_english": "English",
        "permission_manage_subscriptions": "إدارة اشتراكات العملاء",
        "subscriptions_crm_title": "إدارة اشتراكات العملاء 📋",
        "subs_add_instruction": "أرسل اسم العميل",
        "subs_enter_phone": "أرسل رقم الجوال",
        "subs_enter_username": "أرسل يوزر الاشتراك (اسم المستخدم)",
        "subs_enter_password": "أرسل كلمة المرور",
        "subs_enter_subscription_type": "أرسل نوع الاشتراك (مثال: بريميوم)",
        "subs_choose_duration": "اختر مدة الاشتراك بالأيام",
        "subs_enter_custom_duration": "أرسل عدد الأيام (رقم)",
        "subs_choose_start_date": "اختر تاريخ بداية الاشتراك",
        "subs_enter_start_date": "أرسل تاريخ البداية (DD/MM/YYYY أو YYYY-MM-DD)",
        "subs_confirm_dates": (
            "تاريخ البداية: <b>{start}</b>\n"
            "تاريخ النهاية: <b>{end}</b>\n\n"
            "اضغط تأكيد أو عدّل تاريخ النهاية"
        ),
        "subs_enter_end_date": "أرسل تاريخ النهاية (DD/MM/YYYY أو YYYY-MM-DD)",
        "subs_enter_notes": "أرسل ملاحظات إضافية",
        "subs_enter_telegram_id": "أرسل آيدي تيليجرام العميل للتنبيهات",
        "subs_confirm_add": ("تأكيد إضافة العميل:\n\n" "{card}"),
        "subs_customer_added": "تمت إضافة العميل بنجاح ✅",
        "subs_search_choose": "ابحث عن العميل عبر",
        "subs_search_enter_phone": "أرسل رقم الجوال",
        "subs_search_enter_username": "أرسل يوزر الاشتراك",
        "subs_customer_not_found": "لم يتم العثور على العميل ❌",
        "subs_multiple_found": "تم العثور على أكثر من عميل. اختر من القائمة",
        "subs_customer_card": (
            "الاسم: {name}\n"
            "الجوال: <code>{phone}</code>\n"
            "اليوزر: <code>{service_username}</code>\n"
            "الباسورد: <code>{service_password}</code>\n"
            "نوع الاشتراك: {subscription_type}\n"
            "المدة: {duration_days} يوم\n"
            "البداية: {start_date}\n"
            "النهاية: {end_date}\n"
            "الحالة: {status}\n"
            "آيدي تيليجرام: {telegram_user_id}\n"
            "ملاحظات: {notes}"
        ),
        "subs_status_active": "نشط ✅",
        "subs_status_expired": "منتهي ❌",
        "subs_edit_choose_field": "اختر الحقل الذي تريد تعديله",
        "subs_edit_enter_value": "أرسل القيمة الجديدة",
        "subs_customer_updated": "تم تحديث بيانات العميل ✅\n\n{card}",
        "subs_renew_choose_duration": "اختر مدة التجديد",
        "subs_renew_success": (
            "تم تجديد الاشتراك ✅\n" "تاريخ النهاية الجديد: <b>{end_date}</b>"
        ),
        "subs_delete_confirm": ("هل تريد حذف هذا العميل؟\n\n" "{card}"),
        "subs_customer_deleted": "تم حذف العميل ✅",
        "subs_stats_text": (
            "📊 <b>إحصائيات الاشتراكات</b>\n\n"
            "إجمالي العملاء: <b>{total}</b>\n"
            "اشتراكات نشطة: <b>{active}</b>\n"
            "اشتراكات منتهية: <b>{expired}</b>\n"
            "قريبة من الانتهاء: <b>{expiring}</b>"
        ),
        "subs_expiring_list_title": "اشتراكات قريبة من الانتهاء ({count}):",
        "subs_expired_list_title": "اشتراكات منتهية ({count}):",
        "subs_no_customers_in_list": "لا يوجد عملاء في هذه القائمة",
        "subs_offer_settings_title": "إعدادات التنبيهات والعروض 🔔",
        "subs_edit_offer_text": "أرسل نص عرض التجديد الجديد",
        "subs_edit_reminder_template": (
            "أرسل قالب رسالة التنبيه الجديد.\n\n"
            "استخدم المتغيرات التالية (اكتبها كما هي بين أقواس معقوفة):\n"
            "• <code>{name}</code> — اسم العميل\n"
            "• <code>{service_username}</code> — يوزر الاشتراك\n"
            "• <code>{end_date}</code> — تاريخ الانتهاء\n"
            "• <code>{days_left}</code> — الأيام المتبقية\n"
            "• <code>{renewal_offer}</code> — نص عرض التجديد (من الإعدادات)"
        ),
        "subs_edit_reminder_days": "أرسل أيام التنبيه قبل الانتهاء (مفصولة بفاصلة، مثال: 3,1)",
        "subs_settings_saved": "تم حفظ الإعدادات ✅",
        "subs_invalid_phone": "رقم الجوال غير صالح ❌",
        "subs_invalid_date": "تاريخ غير صالح. استخدم DD/MM/YYYY أو YYYY-MM-DD ❌",
        "subs_invalid_duration": "عدد الأيام غير صالح ❌",
        "subs_invalid_telegram_id": "آيدي تيليجرام غير صالح ❌",
        "subs_name_none": "—",
        "subs_notes_none": "—",
        "subs_telegram_none": "غير مرتبط",
        "subs_reminder_owner_message": (
            "📬 <b>تنبيه اشتراك</b> — عميل #{id}\n\n"
            "الاسم: {name}\n"
            "الجوال: <code>{phone}</code>\n"
            "اليوزر: <code>{service_username}</code>\n"
            "الباسورد: <code>{service_password}</code>\n"
            "نوع الاشتراك: {subscription_type}\n"
            "المدة: {duration_days} يوم\n"
            "البداية: {start_date}\n"
            "النهاية: <b>{end_date}</b>\n"
            "متبقي: <b>{days_left}</b> يوم/أيام\n"
            "آيدي تيليجرام: {telegram_user_id}\n"
            "ملاحظات: {notes}\n\n"
            "⬇️ نص الرسالة المرسلة للعميل:\n"
            "{customer_message}\n"
        ),
        "subs_reminder_summary": (
            "📬 ملخص تنبيهات الاشتراكات:\n"
            "تم الإرسال للعميل: {sent_to_customers}\n"
            "تم الإرسال للقناة: {sent_to_channel}\n"
            "فشل الإرسال: {failed}\n"
        ),
        "subs_reminders_running": "جاري تشغيل التنبيهات…",
        "subs_reminders_run_none": (
            "لا توجد اشتراكات تحتاج تنبيهاً الآن "
            "(لا يوجد تطابق لأيام التنبيه أو تم الإرسال مسبقاً اليوم)."
        ),
        "subs_edit_offer_saved": "تم تحديث نص العرض ✅",
        "subs_edit_reminder_template_saved": "تم تحديث قالب رسالة التنبيه ✅",
        "subs_edit_reminder_days_saved": "تم تحديث أيام التنبيه ✅",
        "subs_current_offer": "نص عرض التجديد الحالي:\n\n{text}",
        "subs_current_reminder_template": "قالب رسالة التنبيه الحالي:\n\n{text}",
        "subs_current_reminder_days": "أيام التنبيه الحالية: <b>{days}</b>",
        "subs_exporting_customers": "جاري تصدير العملاء...",
        "subs_customers_exported_success": "تم تصدير العملاء بنجاح ✅",
        "subs_import_instruction": (
            "أرسل ملف Excel (.xlsx) يحتوي على العملاء.\n\n"
            "استخدم <b>تصدير العملاء</b> للحصول على نفس تنسيق الأعمدة.\n"
            "الحقول المطلوبة: الجوال، يوزر الاشتراك، كلمة المرور، المدة، تاريخ البداية.\n"
            "إذا وُجد المعرف مسبقاً يتم تحديث السجل."
        ),
        "subs_importing_customers": "جاري استيراد العملاء...",
        "subs_import_result": (
            "نتيجة الاستيراد:\n"
            "إضافة: <b>{created}</b>\n"
            "تحديث: <b>{updated}</b>\n"
            "تخطي: <b>{skipped}</b>\n"
            "أخطاء: <b>{error_count}</b>"
        ),
        "subs_import_errors_sample": "أمثلة على الأخطاء:\n{lines}",
        "subs_import_invalid_file": "أرسل ملف Excel بصيغة .xlsx فقط ❌",
        "subs_import_no_rows": "الملف فارغ ❌",
        "subs_import_wrong_format": "تنسيق الأعمدة غير صحيح. صدّر العملاء أولاً وعدّل الملف ❌",
        "subs_import_missing_phone": "الجوال مطلوب ❌",
        "subs_import_missing_username": "يوزر الاشتراك مطلوب ❌",
        "subs_import_missing_password": "كلمة المرور مطلوبة ❌",
        "subs_import_nothing_done": "لم يتم استيراد أي سجل. راجع الأخطاء أدناه ❌",
    },
    models.Language.ENGLISH: {
        "user_welcome_msg": "Welcome to the subscription management bot.",
        "admin_welcome_msg": "Subscription admin panel — use the menu below.",
        "force_join_msg": (
            f"You have to join the bot's chat in order to be able to use it\n\n"
            "<b>Join First 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"You have to join the bot's chats in order to be able to use it\n\n"
            "<b>Join all chats 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "join_first_answer": "Join the chat first ❗️",
        "join_all_first_answer": "Join all chats first ❗️",
        "settings": "Settings ⚙️",
        "change_lang": "Choose a language 🌐",
        "change_lang_success": "Language changed ✅",
        "home_page": "Home page 🔝",
        "currently_admin": "You're currently an Admin 🕹",
        "admin_settings_title": "Admin Settings 🪄",
        "add_admin_instruction": (
            "Choose the admin account you want to add by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "admin_added_success": "Admin added successfully ✅",
        "cannot_remove_owner": "You cannot remove the bot owner from the admin list ❗️",
        "admin_removed_success": "Admin removed successfully ✅",
        "remove_admin_instruction": "Choose from the list below the admin you want to remove.",
        "continue_with_admin_command": "To continue press /admin",
        "keyboard_hidden": "Hidden ✅",
        "keyboard_shown": "Shown ✅",
        "ban_instruction": (
            "Choose the user account you want to ban by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "user_not_found": (
            "User not found ❌\n"
            "Make sure of the ID or that the user has started a conversation with the bot before"
        ),
        "user_found": "User found ✅",
        "do_you_want": "Do you want to",
        "operation_success": "Operation completed successfully ✅",
        "ban_confirmation": (
            "User Information:\n"
            "{user_info}\n\n"
            "Current Ban Status: <b>{ban_status}</b>\n\n"
            "This user will be <b>{action}</b>.\n\n"
            "Press the <b>Confirm</b> button to proceed."
        ),
        "user_banned": "Banned 🔒",
        "user_not_banned": "Not Banned 🔓",
        "action_ban": "ban",
        "action_unban": "unban",
        "send_message": "Send the message",
        "send_message_to": "Who do you want to send the message to?",
        "send_user_ids": "Send the user IDs you want to send the message to, one per line.",
        "send_chat_id": "Send the channel/group ID",
        "sending_messages": "The bot is sending messages now, you can continue using it normally",
        "bot_must_be_member": "The bot must be a member of this channel/group to be able to post in it",
        "message_published_success": "Message published in {chat_title} successfully ✅",
        "bot_owner": "Bot Owner",
        "force_join_chats_title": "Manage Force Join Chats 💬",
        "add_force_join_chat_instruction": (
            "Choose the chat you want to force users to join by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "enter_chat_link_instruction": (
            "Chat found: <b>{chat_title}</b>\n\n"
            "Send the chat invite link or username\n\n"
            "Example: https://t.me/channel_name or @channel_name"
        ),
        "force_join_chat_added_success": "Force join chat added successfully ✅",
        "force_join_chat_removed_success": "Force join chat removed successfully ✅",
        "remove_force_join_chat_instruction": "Choose from the list below the chat you want to remove.",
        "no_force_join_chats": "No force join chats currently ❗️",
        "force_join_chats_list_title": "Force Join Chats List",
        "invalid_chat_id": "Invalid chat ID ❌",
        "chat_not_found": "Chat not found ❌\nMake sure of the ID or that the bot is a member of the chat",
        "chat_link_required": "The chat doesn't have an invite link. Please send the invite link manually.",
        "invalid_chat_link": "Invalid chat link ❌\nMust start with https://t.me/ or @",
        "select_permissions_instruction": "Select the permissions you want to grant to this admin",
        "permissions_selected": "Permissions selected successfully ✅",
        "manage_permissions": "Manage Permissions 🔐",
        "edit_admin_permissions": "Edit Admin Permissions 🔐",
        "select_admin_to_edit_permissions": "Select the admin whose permissions you want to edit",
        "current_permissions": "Current Permissions",
        "no_permissions": "No permissions",
        "permission_granted": "Permission granted ✅",
        "permission_revoked": "Permission revoked ✅",
        "cannot_edit_owner_permissions": "You cannot edit the bot owner's permissions ❗️",
        "permission_ban_users": "Ban/Unban Users",
        "permission_broadcast": "Broadcast Messages",
        "permission_manage_force_join": "Manage Force Join Chats",
        "permission_view_ids": "View User/Chat IDs",
        "permission_manage_permissions": "Manage Permissions",
        "permission_manage_admins": "Manage Admins",
        "toggle_permission": "Toggle Permission",
        "all_permissions": "All Permissions",
        "no_permissions_selected": "No permissions selected",
        "no_admins_to_edit": "No admins to edit permissions",
        "you_dont_have_permission_to_manage_permissions": "You don't have permission to manage permissions",
        "you_dont_have_permission_to_manage_admins": "You don't have permission to manage admins",
        "you_dont_have_permission_to_ban_users": "You don't have permission to ban users",
        "you_dont_have_permission_to_broadcast": "You don't have permission to broadcast",
        "you_dont_have_permission_to_manage_force_join": "You don't have permission to manage force join chats",
        "you_dont_have_permission_to_view_ids": "You don't have permission to view user/chat IDs",
        "manage_users_settings_title": "Manage Users 👥",
        "export_users_to_excel": "Export Users to Excel 📊",
        "exporting_users": "Exporting users...",
        "users_exported_success": "Users exported successfully ✅",
        "export_error": "An error occurred while exporting ❌",
        "excel_user_id": "User ID",
        "excel_username": "Username",
        "excel_name": "Name",
        "excel_language": "Language",
        "excel_is_admin": "Is Admin",
        "excel_is_banned": "Is Banned",
        "excel_created_at": "Created At",
        "excel_no_username": "N/A",
        "excel_unknown": "Unknown",
        "excel_yes": "Yes",
        "excel_no": "No",
        "excel_customer_id": "ID",
        "excel_customer_name": "Name",
        "excel_phone": "Phone",
        "excel_service_username": "Service username",
        "excel_service_password": "Password",
        "excel_subscription_type": "Subscription type",
        "excel_duration_days": "Duration (days)",
        "excel_start_date": "Start date",
        "excel_end_date": "End date",
        "excel_telegram_user_id": "Telegram user ID",
        "excel_notes": "Notes",
        "excel_customer_status": "Status",
        "lang_arabic": "Arabic",
        "lang_english": "English",
        "permission_manage_subscriptions": "Manage customer subscriptions",
        "subscriptions_crm_title": "Customer subscriptions CRM 📋",
        "subs_add_instruction": "Send customer name",
        "subs_enter_phone": "Send phone number",
        "subs_enter_username": "Send subscription username",
        "subs_enter_password": "Send password",
        "subs_enter_subscription_type": "Send subscription type (e.g. Premium)",
        "subs_choose_duration": "Choose subscription duration in days",
        "subs_enter_custom_duration": "Send number of days",
        "subs_choose_start_date": "Choose subscription start date",
        "subs_enter_start_date": "Send start date (DD/MM/YYYY or YYYY-MM-DD)",
        "subs_confirm_dates": (
            "Start: <b>{start}</b>\n" "End: <b>{end}</b>\n\n" "Confirm or edit end date"
        ),
        "subs_enter_end_date": "Send end date (DD/MM/YYYY or YYYY-MM-DD)",
        "subs_enter_notes": "Send notes",
        "subs_enter_telegram_id": "Send customer Telegram ID for reminders",
        "subs_confirm_add": ("Confirm adding customer:\n\n" "{card}"),
        "subs_customer_added": "Customer added successfully ✅",
        "subs_search_choose": "Search customer by",
        "subs_search_enter_phone": "Send phone number",
        "subs_search_enter_username": "Send subscription username",
        "subs_customer_not_found": "Customer not found ❌",
        "subs_multiple_found": "Multiple customers found. Choose from the list",
        "subs_customer_card": (
            "Name: {name}\n"
            "Phone: <code>{phone}</code>\n"
            "Username: <code>{service_username}</code>\n"
            "Password: <code>{service_password}</code>\n"
            "Type: {subscription_type}\n"
            "Duration: {duration_days} days\n"
            "Start: {start_date}\n"
            "End: {end_date}\n"
            "Status: {status}\n"
            "Telegram ID: {telegram_user_id}\n"
            "Notes: {notes}"
        ),
        "subs_status_active": "Active ✅",
        "subs_status_expired": "Expired ❌",
        "subs_edit_choose_field": "Choose field to edit",
        "subs_edit_enter_value": "Send new value",
        "subs_customer_updated": "Customer updated successfully ✅\n\n{card}",
        "subs_renew_choose_duration": "Choose renewal duration",
        "subs_renew_success": (
            "Subscription renewed ✅\n" "New end date: <b>{end_date}</b>"
        ),
        "subs_delete_confirm": ("Delete this customer?\n\n" "{card}"),
        "subs_customer_deleted": "Customer deleted ✅",
        "subs_stats_text": (
            "📊 <b>Subscription statistics</b>\n\n"
            "Total customers: <b>{total}</b>\n"
            "Active: <b>{active}</b>\n"
            "Expired: <b>{expired}</b>\n"
            "Expiring soon: <b>{expiring}</b>"
        ),
        "subs_expiring_list_title": "Expiring soon ({count}):",
        "subs_expired_list_title": "Expired subscriptions ({count}):",
        "subs_no_customers_in_list": "No customers in this list.",
        "subs_offer_settings_title": "Reminder & offer settings 🔔",
        "subs_edit_offer_text": "Send new renewal offer text",
        "subs_edit_reminder_template": (
            "Send the new expiry reminder message template.\n\n"
            "Use these placeholders (type them exactly with curly braces):\n"
            "• <code>{name}</code> — customer name\n"
            "• <code>{service_username}</code> — service username\n"
            "• <code>{end_date}</code> — expiry date\n"
            "• <code>{days_left}</code> — days until expiry\n"
            "• <code>{renewal_offer}</code> — renewal offer text (from settings)"
        ),
        "subs_edit_reminder_days": "Send reminder days before expiry (comma-separated, e.g. 3,1)",
        "subs_settings_saved": "Settings saved ✅",
        "subs_invalid_phone": "Invalid phone number ❌",
        "subs_invalid_date": "Invalid date. Use DD/MM/YYYY or YYYY-MM-DD ❌",
        "subs_invalid_duration": "Invalid number of days ❌",
        "subs_invalid_telegram_id": "Invalid Telegram ID ❌",
        "subs_name_none": "—",
        "subs_notes_none": "—",
        "subs_telegram_none": "Not linked",
        "subs_reminder_owner_message": (
            "📬 <b>Subscription reminder</b> — customer #{id}\n\n"
            "Name: {name}\n"
            "Phone: <code>{phone}</code>\n"
            "Username: <code>{service_username}</code>\n"
            "Password: <code>{service_password}</code>\n"
            "Plan: {subscription_type}\n"
            "Duration: {duration_days} days\n"
            "Start: {start_date}\n"
            "End: <b>{end_date}</b>\n"
            "Days left: <b>{days_left}</b>\n"
            "Telegram ID: {telegram_user_id}\n"
            "Notes: {notes}\n\n"
            "⬇️ Message sent to customer:\n"
            "{customer_message}\n"
        ),
        "subs_reminder_summary": (
            "📬 Subscription reminders summary:\n"
            "Sent to customers: {sent_to_customers}\n"
            "Sent to channel: {sent_to_channel}\n"
            "Failed to send: {failed}\n"
        ),
        "subs_reminders_running": "Running reminders…",
        "subs_reminders_run_none": (
            "No subscriptions need a reminder right now "
            "(no match for reminder days, or already sent today)."
        ),
        "subs_edit_offer_saved": "Offer text updated ✅",
        "subs_edit_reminder_template_saved": "Reminder message template updated ✅",
        "subs_edit_reminder_days_saved": "Reminder days updated ✅",
        "subs_current_offer": ("Current renewal offer:\n\n" "{text}"),
        "subs_current_reminder_template": (
            "Current reminder message template:\n\n" "{text}"
        ),
        "subs_current_reminder_days": "Current reminder days: <b>{days}</b>",
        "subs_exporting_customers": "Exporting customers...",
        "subs_customers_exported_success": "Customers exported successfully ✅",
        "subs_import_instruction": (
            "Send an Excel file (.xlsx) with customer rows.\n\n"
            "Use <b>Export customers</b> to get the correct column layout.\n"
            "Required: phone, service username, password, duration, start date.\n"
            "Rows with an existing customer ID will be updated."
        ),
        "subs_importing_customers": "Importing customers...",
        "subs_import_result": (
            "Import result:\n"
            "Created: <b>{created}</b>\n"
            "Updated: <b>{updated}</b>\n"
            "Skipped: <b>{skipped}</b>\n"
            "Errors: <b>{error_count}</b>"
        ),
        "subs_import_errors_sample": "Sample errors:\n{lines}",
        "subs_import_invalid_file": "Send an Excel file (.xlsx) only ❌",
        "subs_import_no_rows": "The file is empty ❌",
        "subs_import_wrong_format": "Invalid column headers. Export customers first and edit that file ❌",
        "subs_import_missing_phone": "Phone is required ❌",
        "subs_import_missing_username": "Service username is required ❌",
        "subs_import_missing_password": "Password is required ❌",
        "subs_import_nothing_done": "No rows were imported. See errors below ❌",
    },
}

BUTTONS = {
    models.Language.ARABIC: {
        "check_joined": "تحقق ✅",
        "bot_channel": "قناة البوت 📢",
        "bot_chat": "محادثة البوت 💬",
        "back_button": "الرجوع 🔙",
        "settings": "الإعدادات ⚙️",
        "lang": "اللغة 🌐",
        "back_to_home_page": "العودة إلى القائمة الرئيسية 🔙",
        "select_admin_button": "اختيار حساب آدمن",
        "select_user_button": "اختيار حساب مستخدم",
        "unban_button": "فك الحظر 🔓",
        "ban_button": "حظر 🔒",
        "add_admin": "إضافة آدمن ➕",
        "remove_admin": "حذف آدمن ✖️",
        "show_admins": "عرض الآدمنز الحاليين 👓",
        "admin_settings": "إعدادات الآدمن 🎛",
        "ban_unban": "حظر/فك حظر 🔓🔒",
        "hide_ids_keyboard": "إخفاء/إظهار كيبورد معرفة الآيديات🪄",
        "broadcast": "رسالة جماعية 👥",
        "everyone": "الجميع 👥",
        "specific_users": "مستخدمين محددين 👤",
        "all_users": "جميع المستخدمين 👨🏻‍💼",
        "all_admins": "جميع الآدمنز 🤵🏻",
        "channel_or_group": "قناة أو مجموعة 📢",
        "force_join_chats": "محادثات الإجبار على الانضمام 💬",
        "force_join_chats_settings": "إعدادات محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat": "إضافة محادثة ➕",
        "remove_force_join_chat": "حذف محادثة ✖️",
        "show_force_join_chats": "عرض المحادثات 👓",
        "select_chat_button": "اختيار محادثة",
        "confirm_button": "تأكيد ✅",
        "bot": "بوت 🤖",
        "channel": "قناة 📢",
        "group": "مجموعة 👥",
        "user": "مستخدم 🆔",
        "manage_permissions": "إدارة الصلاحيات 🔐",
        "edit_permissions": "تعديل الصلاحيات ✏️",
        "skip_button": "تخطي ⬅️",
        "save_button": "حفظ ✅",
        "permission_ban_users": "حظر/فك حظر المستخدمين",
        "permission_broadcast": "إرسال رسائل جماعية",
        "permission_manage_force_join": "إدارة محادثات الإجبار على الانضمام",
        "permission_view_ids": "عرض معرفات المستخدمين/المحادثات",
        "permission_manage_permissions": "إدارة الصلاحيات",
        "permission_manage_admins": "إدارة الآدمنز",
        "manage_users_settings": "إدارة المستخدمين 👥",
        "export_users_to_excel": "تصدير المستخدمين إلى Excel 📊",
        "subscriptions_crm": "إدارة الاشتراكات 📋",
        "subs_add_customer": "إضافة عميل ➕",
        "subs_search": "بحث 🔍",
        "subs_expiring": "قريبة من الانتهاء ⏳",
        "subs_expired": "منتهية ❌",
        "subs_stats": "إحصائيات 📊",
        "subs_offer_settings": "إعدادات العروض 🔔",
        "subs_run_reminders_now": "تشغيل التنبيهات الآن 🔔",
        "subs_export_excel": "تصدير العملاء 📤",
        "subs_import_excel": "استيراد العملاء 📥",
        "subs_search_by_phone": "حسب الجوال 📱",
        "subs_search_by_username": "حسب اليوزر 👤",
        "subs_edit": "تعديل ✏️",
        "subs_renew": "تجديد 🔄",
        "subs_delete": "حذف 🗑",
        "subs_duration_7": "7 أيام",
        "subs_duration_30": "30 يوم",
        "subs_duration_90": "90 يوم",
        "subs_duration_365": "365 يوم",
        "subs_duration_custom": "مدة مخصصة",
        "subs_start_today": "اليوم",
        "subs_start_custom": "تاريخ مخصص",
        "subs_edit_end_date": "تعديل تاريخ النهاية",
        "subs_edit_offer_text_btn": "نص عرض التجديد",
        "subs_edit_reminder_template_btn": "قالب رسالة التنبيه",
        "subs_edit_reminder_days_btn": "أيام التنبيه",
        "permission_manage_subscriptions": "إدارة اشتراكات العملاء",
        "subs_edit_username": "اليوزر",
        "subs_edit_password": "الباسورد",
        "subs_edit_duration": "المدة",
        "subs_edit_end_date_field": "تاريخ النهاية",
        "subs_edit_notes": "ملاحظات",
        "subs_edit_telegram": "آيدي تيليجرام",
        "subs_edit_name": "الاسم",
        "subs_edit_phone": "الجوال",
        "subs_edit_type": "نوع الاشتراك",
    },
    models.Language.ENGLISH: {
        "check_joined": "Verify ✅",
        "bot_channel": "Bot's Channel 📢",
        "bot_chat": "Bot's Chat 💬",
        "back_button": "Back 🔙",
        "settings": "Settings ⚙️",
        "lang": "Language 🌐",
        "back_to_home_page": "Back to home page 🔙",
        "select_admin_button": "Select Admin Account",
        "select_user_button": "Select User Account",
        "unban_button": "Unban 🔓",
        "ban_button": "Ban 🔒",
        "add_admin": "Add Admin ➕",
        "remove_admin": "Remove Admin ✖️",
        "show_admins": "Show Current Admins 👓",
        "admin_settings": "Admin Settings 🎛",
        "ban_unban": "Ban/Unban 🔓🔒",
        "hide_ids_keyboard": "Hide/Show ID Keyboard🪄",
        "broadcast": "Broadcast Message 👥",
        "everyone": "Everyone 👥",
        "specific_users": "Specific Users 👤",
        "all_users": "All Users 👨🏻‍💼",
        "all_admins": "All Admins 🤵🏻",
        "channel_or_group": "Channel or Group 📢",
        "force_join_chats": "Force Join Chats 💬",
        "force_join_chats_settings": "Force Join Chats Settings 💬",
        "add_force_join_chat": "Add Chat ➕",
        "remove_force_join_chat": "Remove Chat ✖️",
        "show_force_join_chats": "Show Chats 👓",
        "select_chat_button": "Select Chat",
        "confirm_button": "Confirm ✅",
        "bot": "Bot 🤖",
        "channel": "Channel 📢",
        "group": "Group 👥",
        "user": "User 🆔",
        "manage_permissions": "Manage Permissions 🔐",
        "edit_permissions": "Edit Permissions ✏️",
        "skip_button": "Skip ⬅️",
        "save_button": "Save ✅",
        "permission_ban_users": "Ban/Unban Users",
        "permission_broadcast": "Broadcast Messages",
        "permission_manage_force_join": "Manage Force Join Chats",
        "permission_view_ids": "View User/Chat IDs",
        "permission_manage_permissions": "Manage Permissions",
        "permission_manage_admins": "Manage Admins",
        "manage_users_settings": "Manage Users 👥",
        "export_users_to_excel": "Export Users to Excel 📊",
        "subscriptions_crm": "Subscriptions CRM 📋",
        "subs_add_customer": "Add customer ➕",
        "subs_search": "Search 🔍",
        "subs_expiring": "Expiring soon ⏳",
        "subs_expired": "Expired ❌",
        "subs_stats": "Statistics 📊",
        "subs_offer_settings": "Offer settings 🔔",
        "subs_run_reminders_now": "Run reminders now 🔔",
        "subs_export_excel": "Export customers 📤",
        "subs_import_excel": "Import customers 📥",
        "subs_search_by_phone": "By phone 📱",
        "subs_search_by_username": "By username 👤",
        "subs_edit": "Edit ✏️",
        "subs_renew": "Renew 🔄",
        "subs_delete": "Delete 🗑",
        "subs_duration_7": "7 days",
        "subs_duration_30": "30 days",
        "subs_duration_90": "90 days",
        "subs_duration_365": "365 days",
        "subs_duration_custom": "Custom duration",
        "subs_start_today": "Today",
        "subs_start_custom": "Custom date",
        "subs_edit_end_date": "Edit end date",
        "subs_edit_offer_text_btn": "Renewal offer text",
        "subs_edit_reminder_template_btn": "Reminder message template",
        "subs_edit_reminder_days_btn": "Reminder days",
        "permission_manage_subscriptions": "Manage subscriptions",
        "subs_edit_username": "Username",
        "subs_edit_password": "Password",
        "subs_edit_duration": "Duration",
        "subs_edit_end_date_field": "End date",
        "subs_edit_notes": "Notes",
        "subs_edit_telegram": "Telegram ID",
        "subs_edit_name": "Name",
        "subs_edit_phone": "Phone",
        "subs_edit_type": "Subscription type",
    },
}


def get_lang(user_id: int):
    with models.session_scope() as s:
        return s.get(models.User, user_id).lang
