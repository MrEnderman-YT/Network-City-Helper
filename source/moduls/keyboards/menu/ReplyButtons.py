# -*- coding: utf8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль")],
    [KeyboardButton(text="Расписание"), KeyboardButton(text="Оценки")],
    [KeyboardButton(text="Д/З на завтра"), KeyboardButton(text="Просрочка")],
    [KeyboardButton(text="Каникулы"), KeyboardButton(text="Звонки")],
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
