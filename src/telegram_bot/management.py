from __main__ import dp, auth
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

async def is_manager(m: Message):
    return m.from_user.username in auth.config['managers']

@dp.message(
    Command("add_customer"),
    is_manager
)
async def add_customer(message: Message):
    await message.answer(
        "Not implemented yet, hahaha"
    )

@dp.message(
    Command("delete_customer"),
    is_manager
)
async def add_customer(message: Message):
    await message.answer(
        "Not implemented yet, hahaha"
    )