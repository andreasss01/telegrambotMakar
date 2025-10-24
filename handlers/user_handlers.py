from aiogram import F,Router
from aiogram.types import Message
from aiogram.filters import CommandStart,Command

from aiogram.types import ChatMemberUpdated


from database.database_manager import Database
from user.respects import give_respect_user,role_given_respect,upgrade_role
from .stat_manager import StatManger
from .profile_manager import ProfileManager
from admin.registraition import register_user
from bot_instance import db

user_router = Router()
stat_manager = StatManger(db)
profile_manager = ProfileManager(db)

@user_router.message(Command("help"))
async def cmd_help(message: Message):
    base_commands = """
help - помощь
/profile - показывает вашу статистку 
 Ответ на сообщение - показывает статистку пользователя на чье сообщение вы ответили
/rep - респект
/stat - статистика бота
/farm - фарм коинов
    

    """
    
    if await db.is_admin(message.from_user.id):
        base_commands += f"""👮 Админ-команды:
/apanel - открыть админ панель
/mute - мут
/warn - варн
/add_rep - выдать репутацию
/reg - принудительная регистрация пользователя в боте(ответ на сообщение )
/give_admin - как ответ на сообщение  /give_admin Уровень \n как обычная команда /give_admin ТГайди Уровень """
    
    await message.answer(base_commands)


# Срабатывает когда меняется статус участника в чате
@user_router.chat_member(F.chat.type != "private")
async def user_joined_chat(event: ChatMemberUpdated):
    # Проверяем что пользователь именно присоединился
    if event.old_chat_member.status == "left" and event.new_chat_member.status == "member":
        user_id = event.new_chat_member.user.id
        username = event.new_chat_member.user.username or event.new_chat_member.user.first_name
        firstname = event.new_chat_member.user.first_name
        checkReg = await db.user_exists(user_id)
        if checkReg:
        # Твоя логика при входе пользователя
            await event.answer(
                f"👋{username} вернулся в беседу!\n"
               
            )
            
        else:
            register = await register_user(user_id,username,firstname)
            if register:
                await event.answer(
                    f"👋Добро пожаловать {username}!\n"
                    f"Используй /help для списка команд"
                )
                await event.answer(register)
                await cmd_help(event)
        # Можно добавить в БД или сделать другие действия
        

@user_router.message(CommandStart())
async def reg_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    firstname = message.from_user.first_name or "No first name"
    register = await register_user(user_id,username,firstname)
    if register:
        await message.answer(register)



@user_router.message(Command("profile"))
async def profile_command(message: Message):
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    profile_text = await profile_manager.get_full_profile(user_id)
    await message.answer(profile_text, parse_mode='HTML')

@user_router.message(Command("stat"))
async def stat_command(message: Message):
    stats_data = await stat_manager.get_system_stats()
    top_respect = await stat_manager.get_top_respect(3)
    
    formatted_message = await stat_manager.format_stats_message(stats_data, top_respect)
    await message.answer(formatted_message, parse_mode='HTML')
    
@user_router.message(Command('add_rep'))
async def add_rep(message : Message):
    if not message.reply_to_message:
        return "Чтобы выдать респект, вы должны ответь на сообщение! \n "
    else:
        respect_amount = "".join(message.text.split()[1:])
        user_id_him_given = message.reply_to_message.from_user.id
        user_id = message.from_user.id
        result = await give_respect_user(user_id_him_given,user_id,respect_amount)
        if result is not None:
            await message.answer(result)
            role = await upgrade_role(user_id_him_given)
            await message.answer(role)
        else:
            await message.answer(result)


@user_router.message(Command('rep'))
async def give_user_respect(message : Message):
    if not message.reply_to_message:
        await message.answer("Чтобы выразить уважение вы должны ответить на сообщения пользователя,к которому хотите проявить уважение!") 
    else:
        himrep = message.reply_to_message.from_user.id
        user_id = message.from_user.id
        if himrep != user_id:
            text = await role_given_respect(user_id,himrep)
            upgrade_respect = await upgrade_role(himrep)
            if text:
                #await message.answer(upgrade_respect)
                await message.answer(text)
                if upgrade_respect:
                    await message.answer(upgrade_respect)
        else:
            await message.answer("Нельзя респектовать самому себе!")

            
