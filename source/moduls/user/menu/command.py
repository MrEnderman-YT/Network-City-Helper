# -*- coding: utf8 -*-
import logging
from aiogram import html, Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.enums import ParseMode

import source.moduls.keyboards.menu.ReplyButtons as kb_menu
import source.moduls.keyboards.auth.InlineButtons as kb_auth

from source.database.check_auth import DB_auth_check
from source.database.check_member import DB_member_check
from source.database.get_privacy import DB_privacy_get

menu_user_command = Router()

logger = logging.getLogger(__name__)


@menu_user_command.message(Command("menu", prefix='/'))
async def command_menu_handler(message: Message) -> None:

    user_id = message.from_user.id

    await message.delete()

    member_check = await DB_member_check().member_check(user_id)
    privacy_check = await DB_privacy_get().privacy_get(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)

    if not member_check or not privacy_check or not auth_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "doesnt exist":
        if privacy_check == "0":
            await message.answer(
                f"👋 Привет, <b>{html.bold(message.from_user.full_name)}</b>! \n\n🤖 <b>Сетевой Город Helper</b> - некоммерческий проект, разработанный для помощи в учебе. \n\n<b>⚙️ Доступные возможности:</b>\n• Уведомления о просроченных заданиях\n• Уведомления о новом расписании\n• Просмотр домашнего задания\n• Просмотр расписания каникул и звонков\n• Калькулятор оценок\n• Отчет об оценках\n\n⛔️ Данный проект <b>не имеет</b> отношения к <b>«ИрТеху»</b>\n\n<b><i>⚠️ Что бы начать пользоваться ботом, вам нужно принять <u>политику конфедициальности</u></i></b>"
                , reply_markup=kb_auth.policy
                , parse_mode=ParseMode.HTML
            )
        elif privacy_check == "1":
            await message.answer(
                f"Что бы начать пользоваться ботом, <b>авторизуйтесь</b> пожалуйста!"
                , reply_markup=kb_auth.auth
                , parse_mode=ParseMode.HTML
            )

    elif auth_check == "exist":
        await message.answer(text=f"<b>Меню было выданно!</b>",
                             parse_mode=ParseMode.HTML, reply_markup=kb_menu.menu)

