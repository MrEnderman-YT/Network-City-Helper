# -*- coding: utf8 -*-
import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from source.database.check_id import DB_id_check
from source.database.add_role import DB_role_add
from source.database.get_role import DB_role_get
from source.database.check_member import DB_member_check
from source.database.get_privacy import DB_privacy_get
from source.database.check_auth import DB_auth_check

from aiogram.enums import ParseMode

give_role_admin_command = Router()

logger = logging.getLogger(__name__)


@give_role_admin_command.message(Command("give_role", prefix='/'))
async def command_give_role_handler(message: Message, command: CommandObject) -> None:
    user_id = message.from_user.id

    await message.delete()

    member_check = await DB_member_check().member_check(user_id)
    privacy_check = await DB_privacy_get().privacy_get(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    role_check = await DB_role_get().role_get(message.from_user.id)

    if not member_check or not role_check or not auth_check or not privacy_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)
        return

    elif role_check != "admin":
        await message.answer(
            text="<b>Вам не доступна данная команда!</b>",
            parse_mode=ParseMode.HTML)
        return

    role_dict = {"admin": "admin", "teacher": "teacher", "student": "student"}
    data = command.args

    if data is None or len(data.split()) != 2:
        await message.answer(
            text="<b>Пожалуйста, укажите имя пользователя и роль.</b>\n"
                 "В формате: <code>/give_role id_пользователя роль</code>",
            parse_mode=ParseMode.HTML)
        return

    user_id, role = data.split()

    if not user_id.isdigit():
        await message.answer(
            text="<b>Пожалуйста, укажите имя пользователя и роль.</b>\n"
                 "В формате: <code>/give_role id_пользователя роль</code>",
            parse_mode=ParseMode.HTML)
        return

    user_id = int(user_id)
    id_check = await DB_id_check().id_check(user_id)

    if not id_check:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)
        return

    elif id_check == "exist":
        if role in role_dict:
            await DB_role_add().role_add(user_id, role_dict[role])
            await message.answer(text=f"<b>Пользователю {user_id} успешно назначена роль {role}!</b>\n",
                                 parse_mode=ParseMode.HTML)
        else:
            await message.answer(text="<b>Указанная роль не найдена!</b>",
                                 parse_mode=ParseMode.HTML)

    elif id_check == "doesnt exist":
        await message.answer(text="<b>Пользователь не был найден!</b>",
                             parse_mode=ParseMode.HTML)