import os
from datetime import datetime

from aiogram.types import Message, FSInputFile

from core.utils.dbconnect import Request


async def get_export_excel_file(message: Message, request: Request):
    file_path = f'{datetime.today().date()}.xlsx'
    try:
        await request.export_to_excel(file_path, message)
        document = FSInputFile(path=file_path)
        await message.answer_document(document=document)
    finally:
        os.remove(file_path)
