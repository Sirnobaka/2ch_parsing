from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

inkb = InlineKeyboardMarkup(row_width=2)
b_tyan = InlineKeyboardButton(text='тян', callback_data='тян')
b_kun = InlineKeyboardButton(text='кун', callback_data='кун')
inkb.row(b_tyan, b_kun)