from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.statesform import StepsForm
from core.utils.dbconnect import Request


async def get_withdrawal(message: Message, state: FSMContext):
    await message.answer(f'Введите код товара для вывода (код должен быть только целым числом)')
    await state.set_state(StepsForm.GET_CODE_WITH)


async def get_code_withdrawal(message: Message, state: FSMContext):
    await message.answer(f'Код товара: {message.text}\r\nТеперь введите количество')
    await state.update_data(code=message.text)
    await state.set_state(StepsForm.GET_QUANTITY_WITH)


async def get_quantity_withdrawal(message: Message, state: FSMContext, request: Request):
    try:
        context_data = await state.get_data()
        code = int(context_data.get('code'))
        await request.withdrawal(code, int(message.text), message)

        data = f'Товар с кодом "{code}" в количестве "{message.text}" успешно выведен.'
        await message.answer(data)

        await state.clear()
    except ValueError:
        await message.answer('Неверно указаны данные.')
