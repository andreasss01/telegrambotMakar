from aiogram import F, Router
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot_instance import db
from admin.registraition import register_user

from admin.warn import WarnManager

import logging
import keyboards.adm_keyboards as kb 



admin_router = Router()
warn_manager = WarnManager(db)

class Register(StatesGroup):
    isApanel = State()


@admin_router.message(Command('apanel'))
async def login_apanel(message : types.Message):
    user_id = message.from_user.id
    if await db.is_admin(user_id) is not False: 
        print(f"{db.is_admin(user_id)}")
        await message.answer("Вы открыли админ панель!",reply_markup=kb.admin_buttons)
    else:
        await message.answer("ПОШЕЛ НАХУЙ СУКА, ТЫ НЕ АДМИН БЛЯДЬ")

@admin_router.callback_query(F.data == 'exit_admin_panel')
async def exit_apanel(callback : CallbackQuery):
    await callback.message.delete()  # Удаляем сообщение с клавиатурой
    await callback.answer("Вы закрыли админ панель!", show_alert=True)

@admin_router.message(Command('reg'))
async def reg_command(message: Message):
    user_id = message.from_user.id
    if await db.is_admin(user_id):
        if message.reply_to_message:
            user_id_target = message.reply_to_message.from_user.id
            username_target = message.reply_to_message.from_user.username
            firstname_target = message.reply_to_message.from_user.first_name
            register = await register_user(user_id_target,username_target,firstname_target)
            if register:
                await message.answer(f"✅Вы принудительно зарегестрировали пользователя: {username_target}")
                await message.answer(register)
    else:
        await message.answer("[AdminSystem] ❌ Вы не админ!")


@admin_router.message(Command('give_admin'))
async def give_admin(message: types.Message ):
    if await db.is_admin(message.from_user.id):
        if not message.reply_to_message:
            himID = " ".join(message.text.split()[1:])
            alevel = "".join(message.text.split()[2:])
            message.answer(alevel)
            admin_id = message.from_user.id
            if await db.is_admin(himID):
                await message.answer("[AdminSystem] ❌ Пользователь уже админ!")
            else:
                given_admin = await db.update_admin_level(himID,alevel)
                if given_admin:
                    await message.answer(given_admin)
        else:
            admin_id = message.from_user.id
            user_id  = message.reply_to_message.from_user.id
            alevel = "".join(message.text.split()[1:])
            if await db.is_admin(user_id):
                await message.answer("[AdminSystem] ❌ Пользователь уже админ!")
            else:
                given_admin = await db.update_admin_level(user_id,alevel)
                if given_admin:
                    await message.answer(given_admin)
    else:
        await message.answer("[AdminSystem] ❌ Вы не админ!")



@admin_router.message(Command('warn'))
async def warn_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("[AdminSystem] ❌ Чтобы выдать варн пропишите /warn причина ")
    else :
        reason = " ".join(message.text.split()[1:]) 
        username_warn =  message.reply_to_message.from_user.username
        user_id_warn =  message.reply_to_message.from_user.id
        admin_id =  message.from_user.id
        chat_id = message.chat.id
        warn = await warn_manager.add_warn(user_id_warn,admin_id,reason,username_warn,chat_id)
        await message.answer(warn,parse_mode='html')
        
        


