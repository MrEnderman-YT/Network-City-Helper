# -*- coding: utf8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from source.database.get_notification import DB_notification_get

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    [InlineKeyboardButton(text="🚪 Выйти", callback_data="logout")],
])

change_stop = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="change_stop")]])


async def create_settings_menu(user_id):
    notification_check = await DB_notification_get().notification_get(user_id)
    if not notification_check:
        return False
    else:
        notification_overdue_assignments = "вкл." if notification_check["notification_overdue_assignments"] else "выкл."
        notification_announcement = "включено" if notification_check["notification_announcement"] else "выключено"
        notification_timetable = "включено" if notification_check["notification_timetable"] else "выключено"
        settings_menu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Уведомление 'Просроченные задания' {notification_overdue_assignments}", callback_data="settings_notification_overdue_assignments")],
            [InlineKeyboardButton(text=f"Уведомление 'События' {notification_announcement}", callback_data="settings_notification_announcement")],
            [InlineKeyboardButton(text=f"Уведомление 'Расписание' {notification_timetable}", callback_data="settings_notification_timetable")],
            [InlineKeyboardButton(text=f"Сменить логин/пароль", callback_data="settings_change")],
            [InlineKeyboardButton(text=f"🔙 Назад", callback_data="settings_back")],

        ])
        return settings_menu
