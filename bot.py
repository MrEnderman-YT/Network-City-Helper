# -*- coding: utf8 -*-
import asyncio

from aiogram import types

from source.moduls.user.start.command import start_user_command
from source.moduls.user.privacy.command import privacy_user_command
from source.moduls.user.menu.command import menu_user_command
from source.moduls.user.logout.command import logout_user_command
from source.moduls.system.error.event import error_system_event
from source.moduls.keyboards.settings.callback_change import change_callback
from source.moduls.keyboards.auth.callback import auth_callback
from source.moduls.keyboards.settings.callback import settings_callback
from source.moduls.user.профиль.command import profile_user_filter
from source.moduls.admin.timetable_download.command import timetable_load_admin_command
from source.moduls.admin.bells_download.command import bells_load_admin_command
from source.moduls.admin.holidays_download.command import holidays_load_admin_command
from source.moduls.admin.give_role.command import give_role_admin_command
from source.moduls.user.расписание.command import timetable_user_filter
from source.moduls.user.звонки.command import bells_user_filter
from source.moduls.user.каникулы.command import holidays_user_filter

from source.moduls.system.antiflood.antiflood import ThrottlingMiddleware

from source.config.cfg import Config

from source.utils.logger import logger

Config.dp.include_routers(start_user_command, privacy_user_command, error_system_event, auth_callback, menu_user_command, logout_user_command, profile_user_filter, settings_callback, change_callback, timetable_load_admin_command, bells_load_admin_command, timetable_user_filter, bells_user_filter, holidays_load_admin_command, holidays_user_filter, give_role_admin_command)


async def main() -> None:

    Config.dp.message.middleware(ThrottlingMiddleware())

    await Config.bot.set_my_commands(commands=Config.commands_menu, scope=types.BotCommandScopeAllPrivateChats())

    await Config.dp.start_polling(Config.bot)

if __name__ == "__main__":

    asyncio.run(main())


