import logging
import traceback
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ErrorEvent

from aiogram.enums import ParseMode

error_system_event = Router()

logger = logging.getLogger(__name__)


@error_system_event.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):

    exc_type, exc_value, exc_traceback = type(event.exception), event.exception, event.exception.__traceback__

    tb_str = "".join(traceback.format_tb(exc_traceback))
    filepath = None
    line_number = None

    for line in tb_str.splitlines():
        if "Network City Helper" in line:
            filepath = line.split("File ")[1].split(",")[0].strip('"').strip("'")
            line_number = int(line.split(", line ")[1].split(",")[0])
            break

    if filepath is None:
        await message.answer(f"<b>Произошла ошибка!!!</b>\n <pre>{event.exception}\nFile: None\nLine: None</pre>",
                             parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"<b>Произошла ошибка!!!</b>\n <pre>{event.exception}\nFile: {filepath}\nLine: {line_number}</pre>",
                             parse_mode=ParseMode.HTML)

    logger.critical("Critical error caused by %s", event.exception, exc_info=False)