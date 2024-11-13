import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.enums import ParseMode

privacy_user_command = Router()

logger = logging.getLogger(__name__)


@privacy_user_command.message(Command("privacy", prefix='/'))
async def command_start1_handler(message: Message) -> None:
    privacy_btn = InlineKeyboardButton(
        text="Открыть",
        url="https://telegra.ph/Politika-konfidencialnosti-10-28-9",
    )

    row_privacy = [privacy_btn]

    rows = [
        row_privacy
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await message.delete()

    await message.answer(text=f"<b>Наша политика конфиденциальности</b>",
                         parse_mode=ParseMode.HTML, reply_markup=markup)

