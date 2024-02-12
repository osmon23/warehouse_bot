import pandas as pd

from decouple import config

import asyncpg
from asyncpg.exceptions import DuplicateDatabaseError

from aiogram.types import Message


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_product(self, product_id, name, quantity):
        query = (f"INSERT INTO {config('DB_NAME')} (id, name, quantity) VALUES ({product_id}, '{name}', {quantity}) "
                 f"ON CONFLICT (id) DO UPDATE SET quantity = {config('DB_NAME')}.quantity + EXCLUDED.quantity")
        await self.connector.execute(query)

    async def get_all_products(self):
        query = f"SELECT * FROM {config('DB_NAME')}"
        return await self.connector.fetch(query)

    async def withdrawal(self, product_id, quantity_to_remove, message: Message):
        current_quantity_query = f"SELECT quantity FROM {config('DB_NAME')} WHERE id = {product_id}"
        current_quantity = await self.connector.fetchval(current_quantity_query)

        if current_quantity is None:
            error_message = f"Товар с id {product_id} не найден на складе."
            await message.answer(error_message)
            raise ValueError(error_message)

        if quantity_to_remove > current_quantity:
            error_message = "Недостаточно товара на складе для вывода указанного количества."
            await message.answer(error_message)
            raise ValueError(error_message)

        new_quantity = current_quantity - quantity_to_remove

        if new_quantity == 0:
            delete_query = f"DELETE FROM {config('DB_NAME')} WHERE id = {product_id}"
            await self.connector.execute(delete_query)
        else:
            update_query = f"UPDATE {config('DB_NAME')} SET quantity = {new_quantity} WHERE id = {product_id}"
            await self.connector.execute(update_query)

    async def export_to_excel(self, file_path, message: Message):
        products = await self.get_all_products()
        if not products:
            await message.answer("Нет данных для экспорта.")
            return
        df = pd.DataFrame(products, columns=['id', 'name', 'quantity'])
        df.to_excel(file_path, index=False)


async def create_database_table():
    connection = await asyncpg.connect(user=config('DB_USER'),
                                       password=config('DB_PASSWORD'),
                                       database='postgres',
                                       host=config('DB_HOST'),
                                       port=config('DB_PORT'))
    try:
        await connection.execute(f"CREATE DATABASE {config('DB_NAME')}")
    except DuplicateDatabaseError:
        pass

    await connection.close()

    connection = await asyncpg.connect(user=config('DB_USER'),
                                       password=config('DB_PASSWORD'),
                                       database=config('DB_NAME'),
                                       host=config('DB_HOST'),
                                       port=config('DB_PORT'))
    await connection.execute(f'''
        CREATE TABLE IF NOT EXISTS {config('DB_NAME')} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            quantity INTEGER
        )
    ''')
    await connection.close()


# pip uninstall et-xmlfile numpy openpyxl pandas python-dateutil pytz six tzdata
