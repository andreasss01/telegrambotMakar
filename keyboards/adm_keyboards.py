from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)

admin_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выдать варн',callback_data='give_warn')],
    [InlineKeyboardButton(text='Послать нахуй',callback_data='give_ban')],
    [InlineKeyboardButton(text='Деавторизоваться',callback_data='exit_admin_panel')]
])