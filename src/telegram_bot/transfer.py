from __main__ import auth, dp, tc, usage_commands
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from login import Login

class Usage(StatesGroup):
    stand_by               = State()        # Стэйт, на который юзер переходит, когда отменяет команду. Также не позволяет запускать комадны в других командах
    ask_transmissions      = State()
    track_transmission     = State()
    create_bill            = State()
    report_problem         = State()


class Bill(StatesGroup):
    stand_by               = State()
    get_bill_items         = State()
    get_bill_mode          = State()
    get_item_positions     = State()
    get_embed_description  = State()
    got_all_desc           = State()
    get_place_measurements = State()
    get_embed_price        = State()
    get_address_type       = State()
    get_address            = State()
    get_payment            = State()


class Report(StatesGroup):
    stand_by               = State()
    get_reason             = State()
    embed_evidence         = State()
    report_complete        = State()


class DataCollector:

    def __init__(self):
        self.iterations = None
        self.item_descriptions = []
        self.item_measures = []
        self.item_weights = []

    def collect(self, what: str | int | float, where: list):
        where.append(what)

    def clear(self, what):
        what.clear()
    
    def undo(self, what):
        if len(what) == 0:
            return False
        what.pop()


dc = DataCollector()

bill_form = {

}

@dp.message(Login.logged_in, Command("cancel"))
async def cancel_operation(message: Message, state: FSMContext):
    if not state == Usage.stand_by:
        message.answer("Отмена операции")
        state.set_state(Usage.stand_by)
        state.set_state(Report.stand_by)
        state.set_state(Bill.stand_by)
        bill_form.clear()

@dp.message(Login.logged_in, Command("help"))
async def give_help(message: Message, state: FSMContext):
    await message.answer("Справка по использованию бота:\n" +
        "\n".join(["— "+command+" : "+description for command, description in usage_commands.items()])
    )

@dp.message(Login.logged_in, Command("list"))
async def give_transmissions(message: Message, state: FSMContext):
    await message.answer("Получение списка отправлений. Пожалуйста, подождите")
    if not tc.list_transmissions():
        message.answer("По вашему номеру договора ничего не найдено.")
    message.send(tc.list_transmissions())             # Как определить юзера?

@dp.message(Login.logged_in, Usage.stand_by, Command("track"))
async def track_transmission(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите номер отправления, которое хотите отследить\n"+
        "\n/cancel для отмены."
    )
    await state.set_state(Usage.track_transmission)

@dp.message(Login.logged_in, Usage.track_transmission)
async def got_transmission_id(message: Message, state: FSMContext):
    await message.answer("Получение информации по отправлению. Пожалуйста, подождите")
    if not tc.get_transmission_status(message.text.lower()):
        message.answer("Заказ не найден. Проверьте номер и попробуйте ещё раз")
    await message.answer(tc.get_transmission_id(message.text.lower()))
    await state.set_state(Usage.stand_by)

@dp.message(Login.logged_in, Usage.stand_by, Command("bill"))
async def new_bill(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите количество позиций.\n" +
        "\n/cancel для отмены."
    )
    await state.set_state(Usage.create_bill)
    await state.set_state(Bill.get_bill_items)

transmission_modes = ["дверь-дверь", "склад-склад", "склад-дверь", "дверь-склад"]
@dp.message(Login.logged_in, Bill.get_bill_items)
async def new_bill(message: Message, state: FSMContext):
    if not isinstance(message.text, int):
        message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    dc.iterations = message.text
    await message.answer(
        "Пожалуйста, введите режим доставки.\n" +
        "\n".join(transmission_modes) +
        "\n\n/cancel для отмены."
    )
    await state.set_state(Bill.get_bill_mode)

@dp.message(Login.logged_in, Bill.get_bill_mode)
async def got_bill_mode(message: Message, state: FSMContext):
    if message.text.lower not in transmission_modes:
        await message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    await bill_form.update({"mode": message.text.lower()})
    await message.answer(
        "Пожалуйста, введите количество мест." +
        "\n/cancel для отмены."
    )
    await state.set_state(Bill.get_embed_description)

@dp.message(Login.logged_in, Bill.get_embed_description)
async def got_bill_positions(message: Message, state: FSMContext):
    if not isinstance(message.text, int):
        await message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    await bill_form.update({"positions": message.text})
    await message.answer(
        "Пожалуйста, введите описание каждого товара по отдельности" +
        "\n\n/confirm — закончить и подтвердить все данные"
        "\n/undo — сброс последней позиции" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
    )
    await state.set_state(Bill.get_bill_description)

item_descriptions = []

@dp.message(Login.logged_in, Bill.get_embed_description, Command("undo"))
async def undo_description(message: Message):
    if dc.undo(item_descriptions) is False:
        return
    await dc.undo(item_measures)
    await message.answer(f"Описание прошлой позиции удалено.")

@dp.message(Login.logged_in, Bill.get_embed_description, Command("retry"))
async def retry_descriptions(message: Message, state: FSMContext):
    await dc.clear(item_descriptions)
    await message.answer("Описания всех позиций стёрты.")

@dp.message(Login.logged_in, Bill.get_embed_description, Command("confirm"))
async def confirm_descriptions(message: Message, state: FSMContext):
    await bill_form.update({"descriptions": item_descriptions})
    await message.answer("Все позиции записаны!")
    await state.set_state(Bill.got_all_desc)

@dp.message(Login.logged_in, Bill.get_embed_description)
async def got_one_description(message: Message, state: FSMContext):
    await item_descriptions.append(message.text)
    await message.answer(
        f"Описание позиции {iterations} записано."+
        "\n\n/confirm — закончить и подтвердить все данные"
        "\n/undo — сброс последней позиции" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
        )   

@dp.message(Login.logged_in, Bill.got_all_desc)
async def ask_measurements(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, напишите измерения каждого места." +
        "\n\n/confirm — закончить и подтвердить все данные"
        "\n/undo — сброс последней позиции" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
    )
    await state.set_state(Bill.get_place_measurements)

@dp.message(Login.logged_in, Bill.get_place_measurements, Command("undo"))
async def undo_measurements(message: Message):
    if dc.undo(item_measures) is False:
        return
    await dc.undo(item_measures)
    await message.answer(f"Описание прошлой позиции удалено.")

@dp.message(Login.logged_in, Bill.get_place_measurements, Command("retry"))
async def retry_measurements(message: Message, state: FSMContext):
    await dc.clear(item_measures)
    await message.answer("Описания всех позиций стёрты.")

@dp.message(Login.logged_in, Bill.get_place_measurements, Command("confirm"))
async def confirm_measurements(message: Message, state: FSMContext):
    await bill_form.update({"measurements": dc.item_measures})
    await message.answer("Все позиции записаны!")
    await state.set_state(Bill.got_all_measurements)

@dp.message(Login.logged_in, Bill.get_place_measurements)
async def collect_one_measure(message: Message):
    await message.answer("Описание ")