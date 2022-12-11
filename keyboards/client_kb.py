from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types

b0 = KeyboardButton('/start')
b1 = KeyboardButton('/info')
b2 = KeyboardButton('/threads')
b3 = KeyboardButton('/find')
b4 = KeyboardButton('/cancel')
b5 = KeyboardButton('/clear')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# add(b1) - to add button below
# incert(b2) - to add button to the right
# row(b1, b2, b3) - to place all buttons in one row 
kb_client.row(b3, b4).row(b0, b1, b2)

b_male = KeyboardButton('кун')
b_female = KeyboardButton('тян')
kb_gender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_gender.row(b_female, b_male)
