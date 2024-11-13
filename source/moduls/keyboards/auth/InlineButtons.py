from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


policy = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📖 Читать", url="https://telegra.ph/Politika-konfidencialnosti-10-28-9")], [InlineKeyboardButton(text="🔘 Принять", callback_data="policy")]])

auth = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Авторизоваться (логин/пароль)", callback_data="auth_login_password")]])

auth_stop = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="auth_stop")]])