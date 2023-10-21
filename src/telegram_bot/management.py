from __main__ import dp, auth
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
import re

async def is_manager(m: Message):
    return m.from_user.username in auth.config['managers']

async def is_admin(m: Message):
    return m.from_user.username in auth.config['admins']

@dp.message(
    Command("add_customer"),
    is_manager
)
async def add_customer(message: Message):
    credentials = message.text.split()
    auth.add_creds(credentials[1], credentials[2])


@dp.message(
    Command("delete_customer"),
    is_manager
)
async def delete_customer(message: Message):
    contract_id = message.text.split()[1]
    if not auth.del_creds(contract_id):
        await message.answer("Клиент не найден")
        return
    
    await message.answer("Данные клиента удалены")

