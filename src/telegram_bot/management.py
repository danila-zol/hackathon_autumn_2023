from __main__ import dp, auth
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

@dp.message(
    Command("add_contract_id"),
    F.from_user.in_(auth.config["managers"])
)
async def add_customer(message: Message):
    message.answer(
        "Not implemented yet, hahaha"
    )