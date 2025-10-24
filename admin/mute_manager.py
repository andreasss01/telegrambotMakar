from aiogram import F, Router
from aiogram import types
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from database.database_manager import Database
from datetime import datetime, timedelta  
from bot_instance import botik,db



mute_router = Router()
bot = botik


async def mute_user(chat_id: int, user_id: int, duration: int, unit: str, reason: str, admin_username: str,username: str):
    """Универсальный метод для мута пользователя"""
    
    # Конвертируем время в секунды и получаем timestamp
    if unit in ["ч", "часов", "час"]:
        dt = datetime.now() + timedelta(hours=duration)
    elif unit in ["м", "минут", "минуты"]:
        dt = datetime.now() + timedelta(minutes=duration)
    else:
        return None  # или выбросить исключение
    
    timestamp = dt.timestamp()
    
    # Выдаём мут через Telegram API
    await bot.restrict_chat_member(
        chat_id, 
        user_id, 
        types.ChatPermissions(can_send_messages=False), 
        until_date=timestamp
    )
    
    # Формируем сообщение
    mute_message = (
        f' | <b>Решение было принято:</b> {admin_username}\n'
        f' | <b>Нарушитель:</b> <a href="tg://user?id={user_id}">{username}</a>\n'
        f'⏰ | <b>Срок наказания:</b> {duration} {unit}\n'
        f' | <b>Причина:</b> {reason}'
    )
    
    return mute_message



@mute_router.message(Command('мут'), F.chat.type != 'private')
async def add_mute(message: Message):
    # Проверка ответа на сообщение
    if not message.reply_to_message:
        await message.answer("[AdminSystem] ❌ Эта команда должна быть ответом на сообщение!")
        return
    
    # Проверка прав админа
    if not await db.is_admin(message.from_user.id):
        await message.answer("[AdminSystem] ❌ Вы не админ!")
        return
    
    # Парсинг аргументов
    try:
        parts = message.text.split()
        muteint = int(parts[1])
        mutetype = parts[2]
        reason = " ".join(parts[3:])
    except (IndexError, ValueError):
        await message.answer("Не хватает аргументов!\nПример:\n`/мут 1 ч причина`")
        return
    
    # Вызов универсального метода мута
    mute_result = await mute_user(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        duration=muteint,
        unit=mutetype,
        reason=reason,
        admin_username=message.from_user.first_name,
        username= message.from_user.username
    )
    
    if mute_result:
        await message.reply(mute_result, parse_mode='html')


@mute_router.message(Command('unmute'), F.chat.type != 'private')
async def unmute_cmd(message: Message):
    if not message.reply_to_message:
        await message.answer("❌ Ответь на сообщение для размута!")
        return
    
    if not await db.is_admin(message.from_user.id):
        await message.answer("❌ Не админ!")
        return

    user_id = message.reply_to_message.from_user.id
    
    # Восстанавливаем все права
    await bot.restrict_chat_member(
        message.chat.id, 
        user_id, 
        types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )
    
    await message.answer(f"✅ {message.from_user.first_name} размутил пользователя")