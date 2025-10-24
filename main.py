from aiogram import Dispatcher
from bot_instance import botik
from bot_instance import db
import asyncio


from handlers.admin_handlers import admin_router
from handlers.user_handlers import user_router
from admin.mute_manager import mute_router
from user.respects import respects_router
from user.roles.role_commands import role_router
from user.roles.role_manager import RoleManager
from coins_system.coin_commands import coin_router


bot = botik
dp = Dispatcher()

async def main():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(mute_router)
    dp.include_router(respects_router)
    dp.include_router(role_router)
    dp.include_router(coin_router)
    print("[MakarBOT] Включен!")
    await db.create_users_table()
    await db.create_warns_table()
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[MakarBOT] Выключен!")
    
