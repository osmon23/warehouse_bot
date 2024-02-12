from decouple import config

from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from core.utils.statesform import StepsForm

enter_token = config('ENTER_TOKEN')


async def get_start(message: Message, state: FSMContext):
    await message.answer(f'Добро пожаловать, {hbold(message.from_user.full_name)}!\n'
                         f'Напишите токен для доступа.')
    await state.set_state(StepsForm.GET_TOKEN)


async def get_enter_token(message: Message, state: FSMContext):
    await state.update_data(token=message.text)
    context_data = await state.get_data()
    token = context_data.get('token')
    if token == enter_token:
        await message.answer(f'Добро пожаловать на склад!')
        await state.clear()
    else:
        await message.answer(f'Неправильный токен, попробуйте еще раз.')


async def get_help(message: Message):
    await message.answer(f'Команды:\n<b>1) /add:</b> Добавить товар на склад. '
                         f'Если код товара уже есть в базе то, количество товара суммируется.'
                         f'То есть, если на складе уже есть товар с кодом: 123, и его количество: 10, '
                         f'добавив товар с таким же кодом: 123, в количестве: 5, в базе будет количество: 15.\n'
                         f'<b>2) /list:</b> Выводит весь список товаров.\n'
                         f'<b>3) /withdrawal:</b> Вывод товара со склада по коду. '
                         f'Нужно указать код и количество товара. Если количество равно нулю, '
                         f'то он удаляеться со склада.\n'
                         f'<b>4) /file:</b> Отправит файл Excel, где весь список товаров на складе.')
