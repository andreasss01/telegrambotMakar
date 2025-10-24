from aiogram import Bot
from database.database_manager import Database

db = Database()

from config import config

botik = Bot(token=config.BOT_TOKEN)