import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from auth import Authenticator
from trans import Transmission, TransChecker
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

dp = Dispatcher()
auth = Authenticator()
tc = TransChecker()

usage_commands = {
    "/list": "Вывести список отправлений",
    "/track": "Узнать статус заказа",
    "/bill": "Создать новую накладную",
    "/report": "Зарегестрировать претензию",
    "/help": "Получить сообщение со справкой",
}

import management
import customer

# @dp.message(F.text)
# async def send_state(message : Message, state : FSMContext):
#     current_state = await state.get_state()
#     print(f"Current state: {current_state}")
#     await message.answer(f"Current state: {current_state}")


async def main():
    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]

    bot = Bot(api_key)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
