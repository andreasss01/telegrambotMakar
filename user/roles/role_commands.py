from aiogram import F,Router,types
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from .role_manager import RoleManager
from bot_instance import db


role_manager = RoleManager(db)
role_router = Router()

@role_router.message(Command('setrole'))
async def give_role(message : Message):
    parts = message.text.split()  # ['/setrole', '1', 'еблан']
    
    if len(parts) < 3:
        await message.answer("❌ Формат: /setrole [user_id] [role_name]")
        return
    
    user_id = parts[1]    # '1'
    new_role = parts[2] 
    result_set = await role_manager.set_user_role(user_id,new_role)
    if result_set:
        await message.answer(result_set)