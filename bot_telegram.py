from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from data_base.update_json import update_json_every
import asyncio
import aioschedule

import os
import json


async def on_startup(_):
    print('Bot is online')
    sqlite_db.sql_start()
    asyncio.create_task(update_json_every(10))

# import handlers from modules
from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
