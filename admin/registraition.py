from bot_instance import db 

async def register_user(user_id,username,firstname) -> str:
    try:

        role = "Участник"
        admin_level = 0

        
        # Проверяем, зарегистрирован ли пользователь
        if await db.user_exists(user_id):
            #logging.info(f"Пользователь {user_id} уже зарегистрирован")
            return False
        else:
            # Регистрируем нового пользователя
            await db.add_user(user_id, username, firstname, admin_level,role)
            #logging.info(f"Новый пользователь: ID={user_id}, Username=@{username}, Name={firstname}, AdminLevel={admin_level}, Role={role}")
            return f"✅ Регистрация успешна!\n👤 ID: {user_id}\n📛🔗 Username: @{username}\n👤 Роль: {role}"
        
    except Exception as e:
        print(f"Ошибка в register_user: {e}")
        raise