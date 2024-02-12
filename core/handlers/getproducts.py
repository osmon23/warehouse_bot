from aiogram.types import Message
from core.utils.dbconnect import Request


async def get_products(message: Message, request: Request):
    products = await request.get_all_products()
    response = "\n".join(
        [f"Код товара: {product['id']}\nНазвание: {product['name']}\nКоличество: {product['quantity']}\n"
         for product in products])
    await message.answer(response)
