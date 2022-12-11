from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb

ID = None

# class FSMAdmin(StatesGroup):
#     #threads = State()
#     gender = State()
#     age = State()
#     city = State()
#     time = State()


# Get moderator's ID to accept access rights
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Hi, admin!', reply_markup=admin_kb.button_case_admin)
    await message.delete()



# # Start to question the user
# #@dp.message_handler(commands='Поиск', state=None)
# async def cm_start(message: types.Message):
#     # this is to check if it's admin or not
#     #if message.from_user.id == ID
#     await FSMAdmin.gender.set()
#     await message.reply('Тян или кун?')


# Register handlers
def register_handlers_admin(dp: Dispatcher):
    # dp.register_message_handler(cm_start, commands=['Find'], state=None)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
