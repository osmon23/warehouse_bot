import sys
import asyncio
import logging
import contextlib

import asyncpg
from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart

from core.handlers.basic import get_start, get_enter_token, get_help
from core.handlers.addproduct import add_product, get_code, get_name_product, get_quantity
from core.handlers.getproducts import get_products
from core.handlers.withdrawal import get_withdrawal, get_code_withdrawal, get_quantity_withdrawal
from core.handlers.excelfile import get_export_excel_file
from core.middlewares.chat_action_middleware import ExampleChatActionMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.utils.statesform import StepsForm
from core.utils.commands import set_commands
from core.utils.dbconnect import create_database_table

token = config('BOT_TOKEN')
admin = config('ADMIN')


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(admin, text='Бот остановлен!')


async def create_pool():
    return await asyncpg.create_pool(user=config('DB_USER'), password=config('DB_PASSWORD'),
                                     database=config('DB_NAME'), host=config('DB_HOST'),
                                     port=config('DB_PORT'), command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token, parse_mode=ParseMode.HTML)
    await create_database_table()
    pool_connect = await create_pool()
    dp = Dispatcher()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(ExampleChatActionMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, CommandStart())
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(get_enter_token, StepsForm.GET_TOKEN)
    dp.message.register(add_product, Command(commands='add'))
    dp.message.register(get_code, StepsForm.GET_CODE)
    dp.message.register(get_name_product, StepsForm.GET_NAME_PR)
    dp.message.register(get_quantity, StepsForm.GET_QUANTITY)
    dp.message.register(get_products, Command(commands='list'))
    dp.message.register(get_withdrawal, Command(commands='withdrawal'))
    dp.message.register(get_code_withdrawal, StepsForm.GET_CODE_WITH)
    dp.message.register(get_quantity_withdrawal, StepsForm.GET_QUANTITY_WITH)
    dp.message.register(get_export_excel_file, Command(commands='file'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
