from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.utils.markdown import hlink
from keyboards import kb_client, kb_gender
from aiogram.types import ReplyKeyboardRemove
#
from data_base import sqlite_db, json_data, parser_functions
#
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


''' ******************** Client part **********************'''


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    channel_id = -1001670729864
    try:
        await bot.send_message(message.from_user.id, 'Good luck!', reply_markup=kb_client)
        #await bot.send_message(channel_id, 'Good luck!')
        # to delete message '/start' from user
        #await message.delete()
    except:
        await message.reply('Write your message to bot dm:\nhttps://t.me/Love2ch_bot')


async def command_help(message: types.Message):
    help_message = "Доступные команды:\n" + "\n" \
        + "/start - приветствие" + "\n" \
        + "/find - начать поиск" + "\n" \
        + "/cancel - прервать поиск" + "\n" \
        + "/clear - удалить результаты последнего поиска" + "\n" \
        + "/info - информация о боте" + "\n" \
        + "/threads - список доступных тредов" + "\n" \
        + "/help - I need somebody heeeeeeelp" + "\n"
    await message.reply(help_message)


async def get_threads(message: types.Message):
    soc_link = hlink('soc - Овощной', 'https://2ch.hk/soc/res/5959967.html')
    hc_link = hlink('hc - Поиск тред', 'https://2ch.hk/hc/res/543463.html')
    links = 'Список доступных тредов:\n' + soc_link + '\n' + hc_link
    # reply_markup=ReplyKeyboardRemove() - to delete keyboard after this answer
    await message.answer(links, parse_mode='HTML', disable_web_page_preview=True)


async def get_info(message: types.Message):
    await message.answer('Этот бот помогает искать анкеты, размещённые на сайте 2ch.hk')



'''********************** User interview *******************************'''
class FSMAdmin(StatesGroup):
    #threads = State()
    gender = State()
    age = State()
    city = State()
    time_period = State()
    clear_messages = State()
    #username = State()
    #mess_id = State()



# Start to question the user
#@dp.message_handler(commands='find', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.gender.set()
    await message.answer('Поиск тянов или кунов (тян, кун)?') #reply_markup=kb_gender


# Exit from state machine
#@dp.message_handler(state="*", commands='cancel')
#@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('OK, canceled')


# Answer the first question: gender
#@dp.message_handler(state=FSMAdmin.gender)
async def input_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text.lower()
    await FSMAdmin.next()
    await message.answer('Возраст (введи диапазон, напиример, 18-22)')


# Answer the second question: age
#@dp.message_handler(state=FSMAdmin.age)
async def input_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        #data['age'] = tuple(map(int, message.text.split('-')))
        data['age'] = message.text.lower()
    await FSMAdmin.next()
    await message.answer('Введи город (желательно - без ошибок) или "все" или "интернет"')


# Answer the third question: city
#@dp.message_handler(state=FSMAdmin.city)
async def input_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.lower()
    await FSMAdmin.next()
    await message.answer('Анкеты за последие ... дней (введи число)', reply_markup=ReplyKeyboardRemove())


# Answer the fourth question: period of time in days
#@dp.message_handler(state=FSMAdmin.time)
async def input_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        #data['time_period'] = float(message.text)
        data['time_period'] = message.text
        data['username'] = message.from_user.username
        data['mess_id'] = message.message_id
    # and now we send the answers to user
    async with state.proxy() as data:
        req_gender = parser_functions.select_gender(data['gender'])
        req_age = parser_functions.strip_age(data['age'])
        req_age_min, req_age_max = 0, 0
        if len(req_age) == 2:
            req_age_min, req_age_max = req_age[0], req_age[1]
        req_city = parser_functions.select_city(data['city'])
        req_time = int(data['time_period'])
        print(req_gender, req_age_min, req_age_max, req_city, req_time, sep=' | ')
        data_out = json_data.filter_data(req_gender, req_age[0], req_age[1], req_city, req_time)
        # list with messages from bot (applications)
        bot_message_ids = []
        for d in data_out:
            bot_message = await message.answer(d)
            print(f'messaege {bot_message.message_id} added')
            bot_message_ids.append(bot_message.message_id)
        #await message.answer(str(data))
        async with state.proxy() as data:
            data['bot_messages'] = bot_message_ids
        await message.answer('Это результаты поиска. Если хочешь их очистить нажми /clear\n'+
            'Чтобы начать новый поиск: /start и затем /find')
    await sqlite_db.sql_add_command(state)
    #await state.finish()
    await FSMAdmin.next()


# @dp.message_handler(commands=['clear'])
async def delete_bot_messages(message: types.Message, state: FSMContext):
    if (message.text == '/clear'):
        async with state.proxy() as data:
            for mes_id in data['bot_messages']:
                await bot.delete_message(message.chat.id, mes_id)
                print(f'messaege {mes_id} deleted')
    #for mes_id in bot_message_ids:
    #    await bot.delete_message(message.chat.id, mes_id)
    #    print(f'messaege {mes_id} deleted')
    #bot_message_ids.clear()
    await message.answer('Можно поискать снова...', reply_markup=kb_client)
    await state.finish()




# Register handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(get_threads, commands=['threads'])
    dp.register_message_handler(get_info, commands=['info'])
    #dp.register_message_handler(delete_bot_messages, commands=['clear'])
    dp.register_message_handler(cm_start, commands=['find'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(input_gender, state=FSMAdmin.gender)
    dp.register_message_handler(input_age, state=FSMAdmin.age)
    dp.register_message_handler(input_city, state=FSMAdmin.city)
    dp.register_message_handler(input_time, state=FSMAdmin.time_period)
    dp.register_message_handler(delete_bot_messages, state=FSMAdmin.clear_messages)