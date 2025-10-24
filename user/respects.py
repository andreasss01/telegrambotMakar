from database.database_manager import Database

from aiogram import F,Router,types
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from bot_instance import db


respects_router = Router()

async def upgrade_role(user_id):
    current_role = await db.get_user_role(user_id)
    respect_amount = await db.get_user_respects(user_id)
    if respect_amount:
        print(f"🔍 ДЕБАГ: user_id={user_id}, current_role={current_role}, respect={respect_amount}")
        
        if current_role == "CustomRole":
            return "Кастомная роль не меняется"
        
        original_role = current_role
        new_role = current_role
        
        # ЛОГИКА ПОВЫШЕНИЯ ДЛЯ ВСЕХ РОЛЕЙ
        if respect_amount >= 100.0 and current_role != "LEGENDARY":
            new_role = "LEGENDARY"
        
        elif respect_amount >= 50.0 and current_role not in ["Свояк", "LEGENDARY"]:
            new_role = "Свояк"
        
        elif respect_amount >= 10.0 and current_role not in ["Бродяга", "Свояк", "LEGENDARY"]:
            new_role = "Бродяга"
        
        print(f"🔍 РЕЗУЛЬТАТ: new_role={new_role}")
        
        if new_role != original_role:
            await db.set_user_role(user_id, new_role)
            return f"🎉 Роль обновлена: {new_role}"
        
        return "Роль не изменилась"
    

async def give_respect_user(user_id_him_given,user_id,respect_amount) -> bool:
    if await db.is_admin(user_id) is not False: 
        if await db.user_exists(user_id_him_given):
            await db.add_user_respect(user_id_him_given,float(respect_amount))      
            #await upgrade_role(user_id_him_given)    
            return f"[AdminSystem] ✅Вы выдали {respect_amount} пользователю {user_id_him_given}"
        else:
            return f"[AdminSystem] ❌Не удалось выдать респекты"
    else: 
        return f"[AdminSystem] ❌Вы не админ!"

async def give_respect(user_id_him_given,respect_amount) -> bool:
    if await db.user_exists(user_id_him_given):
        await db.add_user_respect(user_id_him_given,float(respect_amount))          
        return True
    else:
        return False

async def role_given_respect(user_id, him_res):
    role = await db.get_user_role(user_id)
    
    # Определяем бонус в зависимости от роли
    bonuses = {
        "Участник": 0.2,
        "Бродяга": 0.3, 
        "Свояк": 0.4,
        "Администратор": 0.4,
        "LEGENDARY": 0.5
    }
    
    bonus = bonuses.get(role, 0.2)  # значение по умолчанию
    
    # Выдаём респект ОДИН РАЗ
    success = await give_respect(him_res, bonus)
    
    if not success:
        return "❌ Ошибка выдачи респекта"
    
    # Получаем обновлённый баланс
    respectHim = await db.get_user_respects(him_res)
    
    # Апгрейдим роль
    await upgrade_role(him_res)
    
    return f"✅ Вы выразили уважение! +{bonus} респекта\n🎯 Авторитет: {round(respectHim, 2)}"