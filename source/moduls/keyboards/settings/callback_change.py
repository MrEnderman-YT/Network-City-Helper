# -*- coding: utf8 -*-
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from source.config.cfg import Config
from aiogram.enums import ParseMode

from source.database.check_auth import DB_auth_check
from source.database.check_member import DB_member_check
from source.database.add_auth import DB_auth_add
from source.database.get_privacy import DB_privacy_get

import source.moduls.keyboards.settings.InlineButtons as kb_settings
import source.moduls.keyboards.auth.InlineButtons as kb_auth

from source.netschoolapi.check_auth_netschoolapi import check_netschoolapi

change_callback = Router()

bot = Config.bot


class Change_login(StatesGroup):
    login = State()
    password = State()


@change_callback.callback_query(F.data == "change_stop")
async def change_settings_stop(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.clear()
    await callback.message.edit_text(
        text="Вы отменили смену логина/пароля!", parse_mode=ParseMode.HTML)


@change_callback.callback_query(F.data == "settings_change")
async def change_settings_login(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    member_check = await DB_member_check().member_check(callback.from_user.id)
    auth_check = await DB_auth_check().auth_check(callback.from_user.id, False)
    privacy_check = await DB_privacy_get().privacy_get(callback.from_user.id)

    if not member_check or not privacy_check or not auth_check:
        await callback.message.edit_text(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                                         parse_mode=ParseMode.HTML)
        await state.clear()

    elif auth_check == "doesnt exist":
        await state.clear()
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
        await state.set_state(Change_login.login)
        msg = await callback.message.edit_text(
            text="Отправь мне свой логин от платформы Сетевой Город!",
            reply_markup=kb_settings.change_stop
        )
        await state.update_data(message_id=msg.message_id)


@change_callback.message(Change_login.login)
async def change_settings_input(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    data = await state.get_data()

    member_check = await DB_member_check().member_check(message.from_user.id)
    auth_check = await DB_auth_check().auth_check(message.from_user.id, False)
    privacy_check = await DB_privacy_get().privacy_get(message.from_user.id)

    await message.delete()

    if not member_check or not privacy_check or not auth_check:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"<b>Произошла ошибка во время работы базы данных!</b>"
        )
        await state.clear()

    elif auth_check == "doesnt exist":
        await state.clear()
        if privacy_check == "0":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text=f"👋 Привет, <b>{message.from_user.full_name}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text="Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )

    elif auth_check == "exist":
        await state.set_state(Change_login.password)
        msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text="Отправь мне свой пароль от платформы Сетевой Город!",
            reply_markup=kb_settings.change_stop
        )
        await state.update_data(message_id=msg.message_id)


@change_callback.message(Change_login.password)
async def change_settings(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    member_check = await DB_member_check().member_check(message.from_user.id)
    auth_check = await DB_auth_check().auth_check(message.from_user.id, False)
    privacy_check = await DB_privacy_get().privacy_get(message.from_user.id)

    await message.delete()

    if not member_check or not privacy_check or not auth_check:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"<b>Произошла ошибка во время работы базы данных!</b>"
        )
        await state.clear()

    elif auth_check == "doesnt exist":
        await state.clear()
        if privacy_check == "0":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text=f"👋 Привет, <b>{message.from_user.full_name}</b>!\n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text="Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )
        await state.clear()

    elif auth_check == "exist":
        auth_netschool_check = await check_netschoolapi(data['login'], data['password'])

        if auth_netschool_check == "AuthError":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text=f"<b>Ошибка авторизации! Неверный логин или пароль</b>"
            )
            await state.clear()

        elif auth_netschool_check == "Error":
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text=f"<b>Ошибка авторизации!</b>"
            )
            await state.clear()

        else:
            role, name, surname, clas = auth_netschool_check
            auth_add = await DB_auth_add().auth_add(message.from_user.id, data['login'], data['password'], role, name,
                                                    surname, clas)
            if not auth_add:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"<b>Ошибка авторизации!</b>"
                )
                await state.clear()

            if auth_add == "ok":
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"<b>Вы успешно сменили данные!</b>\n<i>Используй команду /menu</i>"
                )
                await state.clear()
