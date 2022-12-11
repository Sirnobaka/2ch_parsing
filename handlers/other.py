from aiogram import types, Dispatcher
from create_bot import dp


''' ******************** Common part **********************'''

# @dp.message_handler()
async def echo_send(message: types.Message):
    #if message.text == 'Hello':
    # answer in group or direct messages
    await message.answer('Используй команды, чтобы взаимодействовать с ботом!\nЧтобы начать, нажми /start')
    # reply in group or dm
    #await message.reply(message.text)
    # answer directly to user's dm
    #await bot.send_message(message.from_user.id, message.text)

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)