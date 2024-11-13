from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from source.config.cfg import Config
from aiogram.enums import ParseMode

from source.database.check_auth import DB_auth_check
from source.database.check_member import DB_member_check
from source.database.add_auth import DB_auth_add
from source.database.add_privacy import DB_privacy_add
from source.database.get_privacy import DB_privacy_get
from source.netschoolapi.check_auth_netschoolapi import check_netschoolapi

import source.moduls.keyboards.auth.InlineButtons as kb_auth
import source.moduls.keyboards.menu.ReplyButtons as kb_menu

auth_callback = Router()

bot = Config.bot


class Auth_login_password(StatesGroup):
    login = State()
    password = State()


@auth_callback.callback_query(F.data == "policy")
async def auth_stop(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    member_check = await DB_member_check().member_check(user_id)
    auth_check = await DB_auth_check().auth_check(user_id, False)
    privacy_check = await DB_privacy_get().privacy_get(user_id)

    if not privacy_check or not member_check or not auth_check:
        await callback.answer(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)

    elif auth_check == "exist":

        if privacy_check == "0":
            privacy_add = await DB_privacy_add().privacy_add(user_id)
            await callback.answer("Вы приняли политику конфиденциальности!", show_alert=True)

        elif privacy_check == "1":
            await callback.answer("Вы уже приняли политику конфиденциальности!", show_alert=True)

    elif auth_check == "doesnt exist":

        if privacy_check == "0":
            privacy_add = await DB_privacy_add().privacy_add(user_id)
            await callback.answer("Вы приняли политику конфиденциальности!", show_alert=True)
            await callback.message.edit_text(
            text="Что бы начать пользоваться ботом, <b>авторизуйтесь пожалуйста!</b>",
            reply_markup=kb_auth.auth, parse_mode=ParseMode.HTML)

        elif privacy_check == "1":
            await callback.answer("Вы уже приняли политику конфиденциальности!", show_alert=True)
            await callback.message.edit_text(
                text="Что бы начать пользоваться ботом, <b>авторизуйтесь пожалуйста!</b>",
                reply_markup=kb_auth.auth, parse_mode=ParseMode.HTML)


@auth_callback.callback_query(F.data == "auth_stop")
async def auth_stop(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.clear()
    await callback.message.edit_text(
        text="Вы отменили авторизацию!\nЧто бы начать пользоваться ботом, <b>авторизуйтесь пожалуйста!</b>",
        reply_markup=kb_auth.auth, parse_mode=ParseMode.HTML)


@auth_callback.callback_query(F.data == "auth_login_password")
async def auth_login(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    member_check = await DB_member_check().member_check(callback.from_user.id)
    auth_check = await DB_auth_check().auth_check(callback.from_user.id, False)

    if not member_check or not auth_check:
        await callback.message.edit_text(text=f"<b>Произошла ошибка во время работы базы данных!</b>",
                             parse_mode=ParseMode.HTML)
        await state.clear()

    elif auth_check == "doesnt exist":
        await state.set_state(Auth_login_password.login)
        msg = await callback.message.edit_text(
            text="Отправь мне свой логин от платформы Сетевой Город!",
            reply_markup=kb_auth.auth_stop
        )
        await state.update_data(message_id=msg.message_id)

    elif auth_check == "exist":
        await callback.message.edit_text(
            text="Вы уже зарегестрированны!"
        )


@auth_callback.message(Auth_login_password.login)
async def auth_password_input(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    data = await state.get_data()

    member_check = await DB_member_check().member_check(message.from_user.id)
    auth_check = await DB_auth_check().auth_check(message.from_user.id, False)

    await message.delete()

    if not member_check or not auth_check:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"<b>Ошибка авторизации!</b>"
        )
        await state.clear()

    elif auth_check == "doesnt exist":
        await state.set_state(Auth_login_password.password)
        msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text="Отправь мне свой пароль от платформы Сетевой Город!",
            reply_markup=kb_auth.auth_stop
        )
        await state.update_data(message_id=msg.message_id)

    elif auth_check == "exist":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text="Вы уже зарегестрированны!"
        )
        await state.clear()


@auth_callback.message(Auth_login_password.password)
async def auth_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    member_check = await DB_member_check().member_check(message.from_user.id)
    auth_check = await DB_auth_check().auth_check(message.from_user.id, False)

    await message.delete()

    if not member_check or not auth_check:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"<b>Ошибка авторизации!</b>"
        )
        await state.clear()

    elif auth_check == "doesnt exist":
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
            auth_add = await DB_auth_add().auth_add(message.from_user.id, data['login'], data['password'], role, name, surname, clas)
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
                    text=f"<b>Вы успешно зарегестрировались!</b>\n<i>Используй команду /menu</i>"
                )
                await state.clear()

    elif auth_check == "exist":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text="Вы уже зарегестрированны!"
        )
        await state.clear()
