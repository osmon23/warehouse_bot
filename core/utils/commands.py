from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='help',
            description='Помощь',
        ),
        BotCommand(
            command='add',
            description='Добавить товар',
        ),
        BotCommand(
            command='list',
            description='Список всех товаров',
        ),
        BotCommand(
            command='withdrawal',
            description='Вывод товара',
        ),
        BotCommand(
            command='file',
            description='Файл Excel',
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
