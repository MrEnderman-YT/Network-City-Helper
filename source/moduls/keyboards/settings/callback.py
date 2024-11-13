# -*- coding: utf8 -*-
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from source.config.cfg import Config
from aiogram.enums import ParseMode

from source.database.clear_auth import DB_auth_clear
from source.database.check_auth import DB_auth_check
from source.database.check_member import DB_member_check
from source.database.get_privacy import DB_privacy_get
from source.database.add_notification import DB_notification_add
from source.database.get_notification import DB_notification_get
from source.database.get_profile import DB_profile_get

import source.moduls.keyboards.settings.InlineButtons as kb_settings
import source.moduls.keyboards.auth.InlineButtons as kb_auth
from source.moduls.keyboards.settings.InlineButtons import create_settings_menu

import asyncio

settings_callback = Router()

bot = Config.bot


@settings_callback.callback_query(F.data == "logout")
async def logout(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, True)
    auth_clear = await DB_auth_clear().auth_clear(user_id)

    if not member_check or not auth_check or not auth_clear:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "exist":
        await callback.message.edit_text(text=f"<b>Вы уже вышли из аккаунта!</b>",
                                         parse_mode=ParseMode.HTML)
        msg = await callback.message.answer(text=f"Ваша клавиатура была удалени!", parse_mode=ParseMode.HTML,
                                            reply_markup=types.ReplyKeyboardRemove())
        await msg.delete()

    elif auth_check == "doesnt exist":
        await callback.message.edit_text(text=f"<b>Вы вышли из аккаунта!</b>", parse_mode=ParseMode.HTML)
        msg = await callback.message.answer(text=f"Ваша клавиатура была удалени!", parse_mode=ParseMode.HTML,
                                            reply_markup=types.ReplyKeyboardRemove())
        await msg.delete()


@settings_callback.callback_query(F.data == "settings_back")
async def settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    privacy_check = await DB_privacy_get().privacy_get(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await callback.message.edit_text(
                f"👋 Привет, <b>{html.bold(callback.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await callback.message.edit_text(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )

    elif auth_check == "exist":
        profile_check = await DB_profile_get().profile_get(user_id)
        if not profile_check:
            await callback.message.edit_textr(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                                              parse_mode=ParseMode.HTML)
        else:
            role = profile_check["role"]
            name = profile_check["name"]
            surname = profile_check["surname"]
            clas = profile_check["class"]
            if role is None:
                role = "неизвестно"

            elif name is None:
                name = "неизвестно"

            elif surname is None:
                surname = "неизвестно"

            elif clas is None:
                clas = "неизвестно"

            await callback.message.edit_text(
                text=f"<b>┏┫★ ПРОФИЛЬ:</b>\n\n<b>👤 • Никнейм:</b>   <code>{callback.from_user.full_name}</code>\n<b>🔑 • ID:</b>   <code>{callback.from_user.id}</code>\n<b>⚡️ • Статус:</b>   <code>{role}</code>\n<b>🎫 • Имя:</b>   <code>{name}</code>\n<b>🎫 • Фамилия:</b>   <code>{surname}</code>\n<b>🏫 • Школа:</b>   <code>МБОУ СОШ № 99 г. Челябинска</code>\n<b>🧰 • Класс:</b>   <code>{clas}</code>"
                , reply_markup=kb_settings.settings
                , parse_mode=ParseMode.HTML)


@settings_callback.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    privacy_check = await DB_privacy_get().privacy_get(user_id)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await callback.message.edit_text(
                f"👋 Привет, <b>{html.bold(message.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await callback.message.edit_text(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )
    elif auth_check == "exist":
        settings_menu_kb = await create_settings_menu(user_id)
        await callback.message.edit_text(
            text="<b>┏┫★ НАСТРОЙКИ:</b>\n\n<b>🔔 • Настройте уведомления:</b>\n┗┫Уведомления о просроченных заданиях.\n┗┫Будьте в курсе событий.\n┗┫Узнавайте о новом расписании.\n\n<b>🔐 • Измените свои данные:</b>\n┗┫Можете сменить пароль.\n┗┫Можете обновить логин."
            , reply_markup=settings_menu_kb
            , parse_mode=ParseMode.HTML
        )


@settings_callback.callback_query(F.data == "settings_notification_overdue_assignments")
async def settings_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    privacy_check = await DB_privacy_get().privacy_get(user_id)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await callback.message.edit_text(
                f"👋 Привет, <b>{html.bold(message.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await callback.message.edit_text(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )
    elif auth_check == "exist":
        await DB_notification_add().notification_add(callback.from_user.id, "notification_overdue_assignments")
        notification_get = await DB_notification_get().notification_get(callback.from_user.id)
        notification_overdue_assignments = "включили" if notification_get[
            "notification_overdue_assignments"] else "выключили"

        settings_menu_kb = await create_settings_menu(user_id)
        await callback.message.edit_text(
            text=f"<b>┏┫★ НАСТРОЙКИ:</b>\n\n<b>🔔 • Настройте уведомления:</b>\n┗┫Уведомления о просроченных заданиях.\n┗┫Будьте в курсе событий.\n┗┫Узнавайте о новом расписании.\n\n<b>🔐 • Измените свои данные:</b>\n┗┫Можете сменить пароль.\n┗┫Можете обновить логин.\n\n💾 • <i>Вы успешно {notification_overdue_assignments} уведомления 'Просроченные задания'</i>"
            , reply_markup=settings_menu_kb
            , parse_mode=ParseMode.HTML
        )


@settings_callback.callback_query(F.data == "settings_notification_announcement")
async def settings_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    privacy_check = await DB_privacy_get().privacy_get(user_id)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await callback.message.edit_text(
                f"👋 Привет, <b>{html.bold(message.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await callback.message.edit_text(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )
    elif auth_check == "exist":
        await DB_notification_add().notification_add(callback.from_user.id, "notification_announcement")
        notification_get = await DB_notification_get().notification_get(callback.from_user.id)
        notification_announcement = "включили" if notification_get["notification_announcement"] else "выключили"

        settings_menu_kb = await create_settings_menu(user_id)

        await callback.message.edit_text(
            text=f"<b>┏┫★ НАСТРОЙКИ:</b>\n\n<b>🔔 • Настройте уведомления:</b>\n┗┫Уведомления о просроченных заданиях.\n┗┫Будьте в курсе событий.\n┗┫Узнавайте о новом расписании.\n\n<b>🔐 • Измените свои данные:</b>\n┗┫Можете сменить пароль.\n┗┫Можете обновить логин.\n\n💾 • <i>Вы успешно {notification_announcement} уведомления 'События'</i>"
            , reply_markup=settings_menu_kb
            , parse_mode=ParseMode.HTML
        )


@settings_callback.callback_query(F.data == "settings_notification_timetable")
async def settings_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    privacy_check = await DB_privacy_get().privacy_get(user_id)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await callback.message.edit_text(
                f"👋 Привет, <b>{html.bold(message.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await callback.message.edit_text(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )
    elif auth_check == "exist":
        await DB_notification_add().notification_add(callback.from_user.id, "notification_timetable")

        notification_get = await DB_notification_get().notification_get(callback.from_user.id)
        notification_timetable = "включили" if notification_get["notification_timetable"] else "выключили"

        settings_menu_kb = await create_settings_menu(user_id)

        await callback.message.edit_text(
            text=f"<b>┏┫★ НАСТРОЙКИ:</b>\n\n<b>🔔 • Настройте уведомления:</b>\n┗┫Уведомления о просроченных заданиях.\n┗┫Будьте в курсе событий.\n┗┫Узнавайте о новом расписании.\n\n<b>🔐 • Измените свои данные:</b>\n┗┫Можете сменить пароль.\n┗┫Можете обновить логин.\n\n💾 • <i>Вы успешно {notification_timetable} уведомления 'Новое расписание'</i>"
            , reply_markup=settings_menu_kb
            , parse_mode=ParseMode.HTML
        )
