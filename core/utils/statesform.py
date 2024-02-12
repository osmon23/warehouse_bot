from aiogram.fsm.state import State, StatesGroup


class StepsForm(StatesGroup):
    GET_TOKEN = State()
    GET_NAME_PR = State()
    GET_QUANTITY = State()
    GET_CODE = State()
    GET_CODE_WITH = State()
    GET_QUANTITY_WITH = State()
