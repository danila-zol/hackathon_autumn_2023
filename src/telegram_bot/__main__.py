import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()

@dp.message(CommandStart())
async def begin(message: Message) -> None:
    await message.answer(
        f"Добро пожаловать, {hbold(message.from_user.full_name)}!\n" +
        "Я — Эфирный Курьер." + 
        "Я помогу вам быстро и удобно составить накладную, отследить заказ или составить жалобу." +
        "Для начала авторизуйтесь."
    )

@dp.message(Command("add_user"))
async def add_user(message: Message) -> None:
    await message.answer("Пожалуйста, введите номер договора.")

    


if __name__ == "__main__":

    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]