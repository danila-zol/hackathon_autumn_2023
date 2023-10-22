from __main__ import auth, dp, tc, usage_commands
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from login import Login

class Usage(StatesGroup):
    stand_by                  = State()        # Стэйт, на который юзер переходит, когда отменяет команду. Также не позволяет запускать комадны в других командах
    list_transmissions        = State()
    track_transmission        = State()
    create_bill               = State()
    report_problem            = State()


class Bill(StatesGroup):
    stand_by                  = State()
    get_bill_items            = State()
    get_bill_mode             = State()
    get_item_positions        = State()
    get_embed_description     = State()
    got_all_desc              = State()
    record_place_measurements = State()
    got_all_measurements      = State()
    record_weights            = State()
    got_all_weights           = State()
    record_place_cost         = State()
    record_costs              = State()
    got_costs                 = State()
    get_address               = State()
    get_payment_type          = State()
    confirm                   = State()


class Report(StatesGroup):
    stand_by                  = State()
    get_reason                = State()
    embed_evidence            = State()
    report_complete           = State()


# class DataCollector:

#     def __init__(self):
#         self.iterations = None
#         self.counter = None
#         self.item_descriptions = []
#         self.item_measures = []
#         self.item_weights = []

#     def clear(self, what):
#         what.clear()
    
#     def undo(self, what):
#         if len(what) == 0:
#             return False
#         what.pop()


# dc = DataCollector()

# bill_form = {

# }
@dp.message(Login.logged_in)
async def initialize(message: Message, state: FSMContext):
    await state.set_state(Usage.stand_by)

@dp.message(Login.logged_in, Command("cancel"))
async def cancel_operation(message: Message, state: FSMContext):
    await message.answer("Отмена операции")
    await state.set_state(Usage.stand_by)
    await state.set_state(Report.stand_by)
    await state.set_state(Bill.stand_by)

@dp.message(Login.logged_in, Command("help"))
async def give_help(message: Message, state: FSMContext):
    await message.answer("Справка по использованию бота:\n" +
        "\n".join(["— "+command+" : "+description for command, description in usage_commands.items()])
    )

@dp.message(Login.logged_in, Command("list"))
async def give_transmissions(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер вашего договора")
    await state.set_state(Usage.list_transmissions)

@dp.message(Login.logged_in, Usage.list_transmissions)
async def list_transmissions(message: Message, state: FSMContext):
    await message.answer("Получение списка отправлений. Пожалуйста, подождите")
    if not tc.list_transmissions(message.text.lower()):
        await message.answer("По вашему номеру договора ничего не найдено.")
    await message.send(tc.list_transmissions(message.text.lower()))
    await state.set_state(Usage.stand_by)

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
        "Пожалуйста, введите режим доставки.\n" +
        "\n/cancel для отмены."
    )
    await state.set_state(Usage.create_bill)
    # await state.set_state(Bill.get_bill_items)

# @dp.message(Login.logged_in, Bill.get_bill_items)
# async def got_bill_items(message: Message, state: FSMContext):
#     if not isinstance(message.text, int):
#         message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
#         return

#     await message.answer(
#         "Пожалуйста, введите режим доставки.\n" +
#         "\n".join(transmission_modes) +
#         "\n\n/cancel для отмены."
#     )
    await state.set_state(Bill.get_bill_mode)

transmission_modes = ["дверь-дверь", "склад-склад", "склад-дверь", "дверь-склад"]
@dp.message(Login.logged_in, Bill.get_bill_mode)
async def got_bill_mode(message: Message, state: FSMContext):
    if message.text.lower not in transmission_modes:
        await message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    await state.update_data(mode=message.text.lower())
    await message.answer(
        "Пожалуйста, введите количество мест." +
        "\n/cancel для отмены."
    )
    await state.set_state(Bill.get_embed_description)

@dp.message(Login.logged_in, Bill.get_embed_description)
async def got_bill_positions(message: Message, state: FSMContext):
    if not any(map(str.isdigit, message.text)):
        await message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    await state.update_data(positions=message.text)
    await state.update_data(descriptions=[])
    await message.answer(
        "Пожалуйста, введите описание каждого товара по отдельности" +
        "\n\n/confirm — закончить и подтвердить все данные"
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
    )
    await state.set_state(Bill.get_bill_description)

# item_descriptions = []

# @dp.message(Login.logged_in, Bill.get_embed_description, Command("undo"))
# async def undo_description(message: Message):
#     if dc.undo(item_descriptions) is False:
#         return
#     dc.counter = await (dc.counter - 1)
#     await dc.undo(dc.item_measures)
#     await message.answer(f"Описание позиции {dc.counter} удалено.")

@dp.message(Login.logged_in, Bill.get_embed_description, Command("retry"))
async def retry_descriptions(message: Message, state: FSMContext):
    # await dc.clear(item_descriptions)
    # dc.counter = await 1
    await state.update_data(descriptions=[])
    await message.answer("Описания всех позиций стёрты.")

@dp.message(Login.logged_in, Bill.get_embed_description, Command("confirm"))
async def confirm_descriptions(message: Message, state: FSMContext):
    await message.answer("Все позиции записаны!")
    await state.set_state(Bill.got_all_desc)

@dp.message(Login.logged_in, Bill.get_embed_description)
async def got_one_description(message: Message, state: FSMContext):
    temp = await state.get_data()["descriptions"]
    await temp.append(message.text)
    await state.update_data(descriptions=temp)
    await message.answer(
        "Описание позиции записано."+
        "\n\n/confirm — закончить и подтвердить все данные"
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
        )   
    # dc.counter = await dc.counter + 1

@dp.message(Login.logged_in, Bill.got_all_desc)
async def ask_measurements(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, напишите измерения каждого места в формате \"[длина]/[ширина]/[высота]\"" +
        "\n\n/confirm — закончить и подтвердить все данные" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
    )
    await state.update_data(measurements=[])
    await state.set_state(Bill.record_place_measurements)

# @dp.message(Login.logged_in, Bill.record_place_measurements, Command("undo"))
# async def undo_measurements(message: Message):
#     if dc.undo(dc.item_measures) is False:
#         return
#     dc.counter = await (dc.counter - 1)
#     await dc.undo(dc.item_measures)
#     await message.answer(f"Описание позиции {dc.item_measures} удалено.")

@dp.message(Login.logged_in, Bill.record_place_measurements, Command("retry"))
async def retry_measurements(message: Message, state: FSMContext):
    # await dc.clear(dc.item_measures)
    # dc.counter = await 1
    await state.update_data(measurements=[])
    await message.answer("Описания всех позиций стёрты.")

@dp.message(Login.logged_in, Bill.record_place_measurements, Command("confirm"))
async def confirm_measurements(message: Message, state: FSMContext):
    await message.answer("Все позиции записаны!")
    await state.set_state(Bill.got_all_measurements)

@dp.message(Login.logged_in, Bill.record_place_measurements)
async def collect_one_measure(message: Message, state: FSMContext):
    meas_dict = await {"Длина": None, "Ширина": None, "Высота": None}
    tokenize_this = await message.text.lower()
    i = await 0
    for _ in range(len(message.text.lower())):
        if message.text[_+1] == "/":
            await meas_dict.update({meas_dict.keys()[i]:tokenize_this[:_+1]})
            i = await i + 1
            tokenize_this[_+1:]
    for measurement in meas_dict.values():
        if measurement is None:
            await message.answer("Некорректный ввод. Пожалуйста повторите попытку.")
            return
    temp = await state.get_data()["measurements"]
    await temp.append(meas_dict)
    await state.update_data()
    await message.answer(
        "Измерения места записаны." +
        "\n\n/confirm — закончить и подтвердить все данные" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
        )

@dp.message(Login.logged_in, Bill.got_all_measurements)
async def ask_weights(message: Message, state: FSMContext):
    await state.update_data(weights=[])
    await message.answer(
        "Пожалуйста, напишите вес каждого места" +
        "\n\n/confirm — закончить и подтвердить все данные" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
    )
    await state.set_state(Bill.record_weights)

@dp.message(Login.logged_in, Bill.record_weights, Command("retry"))
async def retry_weights(message: Message, state: FSMContext):
    # await dc.clear(item_descriptions)
    # dc.counter = await 1
    await state.update_data(weights=[])
    await message.answer("Описания всех позиций стёрты.")

@dp.message(Login.logged_in, Bill.record_weights, Command("confirm"))
async def confirm_weights(message: Message, state: FSMContext):
    await message.answer("Все позиции записаны!")
    await state.set_state(Bill.got_all_weights)

@dp.message(Login.logged_in, Bill.record_weights)
async def got_one_weight(message: Message, state: FSMContext):
    temp = await state.get_data()["weights"]
    await temp.append(message.text.lower())
    await message.answer(
        "Вес места записан." +
        "\n\n/confirm — закончить и подтвердить все данные" +
        "\n/retry — начать набор данных сначала" +
        "\n/cancel — отмена создания накладной"
        )

@dp.message(Login.logged_in, Bill.got_all_weights)
async def ask_place_cost_type(message: Message, state: FSMContext):
    await message.answer("Укажите стоимость вложения:\n— Общая\n— По местам")
    await state.set_state(Bill.record_place_cost)

@dp.message(Login.logged_in, Bill.record_place_cost)
async def get_place_cost_type(message: Message, state: FSMContext):
    if message.text.lower() == "общая":
        await state.update_data(cost_for_all=True)
    elif message.text.lower() == "по местам":
        await state.update_data(cost_for_all=False)
    else:
        await message.ansewr("Некорректный ввод. Пожалуйста, повторите попытку.")
        return 
    await state.update_data(place_cost=None)
    await message.answer("Хорошо. Теперь введите стоимость вложения")
    await state.set_state(Bill.record_costs)

@dp.message(Login.logged_in, Bill.record_costs, Command("retry"))
async def retry_place_cost(message: Message, state: FSMContext):
    await state.update_data(place_cost=None)
    await message.answer("Данные по стоимости стёрты")

@dp.message(Login.logged_in, Bill.record_costs, Command("confirm"))
async def confirm_place_cost(message: Message, state: FSMContext):
    await message.answer("Данные по стоимости записаны")
    await state.set_state(Bill.got_costs)

@dp.message(Login.logged_in, Bill.record_costs)
async def get_place_cost(message: Message, state: FSMContext):
    if state.get_data()["cost_for_all"]:
        await state.update_data(place_cost=[message.text.lower()])
        await message.answer("Стоимость места записана.")   
        await state.set_state(Bill.got_costs)
        return
    else:
        temp = await state.get_data()["place_cost"]
        await temp.append(message.text.lower())
        await state.update_data(place_cost=temp)
        await message.answer("Стоимость места записана\n\n/confirm — закончить и подтвердить запись\n/retry — начать сначала")

@dp.message(Login.logged_in, Bill.got_costs)
async def ask_address(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, укажите адрес. Дополнительно укажите в начале, если это ПВЗ")
    await state.set_state(Bill.get_address)

@dp.message(Login.logged_in, Bill.get_address)
async def got_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Хорошо. Теперь укажите тип оплаты:\n— Оплата получателем\n— Отправителем по договору")
    await state.set_state(Bill.get_payment_type)

@dp.message(Login.logged_in, Bill.get_payment_type)
async def got_payment_type(message: Message, state: FSMContext):
    await state.update_data(payment_type=message.text.lower())
    final_data = await state.get_data()
    await message.answer("Отлично! Теперь пересмотрите введённые данные и подтвердите их командой /confirm\nили начните сначала командой /cancel")
    embeded = await '\n'.join(final_data['descriptions'])
    measurements = await '\n'.join([final_data['measurements']])
    weights = await '\n'.join(final_data['weights'])
    embeded_costs = await '\n'.join(final_data['place_cost'])
    await message.answer(
        f"Режим доставки: {final_data['mode']}\n" +
        f"Количество мест: {final_data['positions']}\n" +
        f"Описание вложений: \n\n{embeded}\n" + 
        f"Габариты вложений каждого места: \n\n{measurements}\n" +
        f"Вес каждого вложения: \n\n{weights}\n" +
        f"Стоимость вложения: {embeded_costs}\n" +
        f"Точный адрес доставки: {final_data['address']}\n" +
        f"Способ оплаты: {final_data['payment_type']}"
    )
    await state.set_state(Bill.confirm)

@dp.message(Login.logged_in, Bill.confirm, Command("confirm"))
async def confirmed(message: Message, state: FSMContext):
    await tc.create_bill(state.get_data())
    await message.answer("Накладная создана!")
    await state.set_state(Bill.stand_by)
    await state.set_state(Usage.stand_by)
