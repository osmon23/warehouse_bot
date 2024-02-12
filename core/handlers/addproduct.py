from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.statesform import StepsForm
from core.utils.dbconnect import Request


async def add_product(message: Message, state: FSMContext):
    await message.answer(f'Введите код товара (код должен быть только целым числом)')
    await state.set_state(StepsForm.GET_CODE)


async def get_code(message: Message, state: FSMContext):
    await message.answer(f'Введите название товара')
    await state.update_data(code=message.text)
    await state.set_state(StepsForm.GET_NAME_PR)


async def get_name_product(message: Message, state: FSMContext):
    await message.answer(f'Название товара: {message.text}\r\nТеперь введите количество')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_QUANTITY)


async def get_quantity(message: Message, state: FSMContext, request: Request):
    context_data = await state.get_data()
    code = int(context_data.get('code'))
    name = context_data.get('name')
    await request.add_product(code, name, message.text)

    data = f'Товар с кодом "{code}" успешно добавлен.'
    await message.answer(data)

    await state.clear()
