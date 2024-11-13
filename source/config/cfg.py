# -*- coding: utf8 -*-
import aiogram

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.types import BotCommand

from source.utils.dotenv_utils import get_dotenv_data


class Config:

    env_data = get_dotenv_data()

    bot = Bot(token=env_data.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    commands_menu = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="logout", description="Выйти из аккаунта"),
        BotCommand(command="menu", description="Меню бота"),
    ]

    dp = Dispatcher()
