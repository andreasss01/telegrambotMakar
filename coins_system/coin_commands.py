from aiogram import F,Router,types
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from .coin_manager import CoinManager
from bot_instance import db

coin_manager = CoinManager(db)
coin_router = Router()

@coin_router.message(Command('farm'))
async def command_farm(message: types.Message):
    user_id = message.from_user.id
    balance = await coin_manager.get_balance(user_id)
    farm = await coin_manager.farm_coins(user_id)
    if farm[0] == 0:
        await message.answer(farm[1])
    else:
        await message.answer(farm[1])