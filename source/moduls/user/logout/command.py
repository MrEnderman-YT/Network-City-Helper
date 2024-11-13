# -*- coding: utf8 -*-
import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.enums import ParseMode

from source.database.clear_auth import DB_auth_clear
from source.database.check_auth import DB_auth_check
from source.database.check_member import DB_member_check

logout_user_command = Router()

logger = logging.getLogger(__name__)


@logout_user_command.message(Command("logout", prefix='/'))
async def command_logout_handler(message: Message) -> None:

    user_id = message.from_user.id

    await message.delete()

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, True)
    auth_clear = await DB_auth_clear().auth_clear(user_id)

    if not member_check or not auth_check or not auth_clear:
        await message.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)
    elif auth_check == "exist":
        await message.answer(text=f"<b>Вы вышли из аккаунта!</b>",
                             parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    elif auth_check == "doesnt exist":
        await message.answer(text=f"<b>Вы уже вышли из аккаунта!</b>",
                             parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
