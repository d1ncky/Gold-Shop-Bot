import random
import sqlite3 as sql

from datetime import *

from aiogram.types import InputFile

from aiogram import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboards
import requests
import json
import urllib.request
from aiogram.utils.exceptions import Throttled
import db_help

import asyncio
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import func
from glQiwiApi import QiwiP2PClient
from glQiwiApi.qiwi.clients.p2p.types import Bill


# ======

skin = 'f/s tactical st' #в кавычки вписать через название скина для вывода

TOKEN = ""
adminid =  #вписать айди админа

# ======

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    suma = State()
    vivod = State()
    screen = State()
    pay = State()
    otziv = State()
# ======


from aiogram.utils.deep_linking import get_start_link


# ======

#f = open('golds.txt','r')
#pricegold = str(*f)

channel = '' #в кавычки вписать канал бота

qiwi_p2p_client = QiwiP2PClient(shim_server_url="play.nanix.fun:80", secret_p2p="")#в кавычки вписать секретный киви p2p ключ купить можно @ms_shop_robot


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    print(message.text[7:])
    if ' ' in message.text and message.chat.id!=message.text[7:]:
        if db_help.check_user(message.from_user.id) == None:
            db_help.add_ref(message.text[7:])
            await bot.send_message(message.text[7:], f"🔔 У вас новый реферал.\n\n❓ Проверить число рефералов можно в профиле.")
            await bot.send_message(adminid, f"🔔 Новый пользователь!\n\n🛠 ID [{message.chat.id} - {message.from_user.first_name}] пригласил [{message.text[7:]} - {db_help.check_user(message.from_user.id)[1]}]")

            db_help.register_user(message.chat.id, message.from_user.first_name)

            await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())
        else:
            await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())
    else:
        if db_help.check_user(message.from_user.id) == None:
            db_help.register_user(message.chat.id, message.from_user.first_name)
            await bot.send_message(adminid, f"🔔 Новый пользователь!\n\n🛠 ID [{message.chat.id} - {message.from_user.first_name}]")
            await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())
        else:
            await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())

@dp.callback_query_handler(text="buygold")
async def test(call: types.CallbackQuery):
    pricegold = float(db_help.goldsc()[1])
    await call.message.edit_text(f"Введите кол-во голды для покупки\n\nВаш баланс - {db_help.check_user(call.from_user.id)[4]} голды/{db_help.check_user(call.from_user.id)[3]} рублей\n\nКурс голды - {pricegold}")
    await UserState.suma.set()


@dp.callback_query_handler(text="vivodgold")
async def test(call: types.CallbackQuery):
    await call.message.edit_text(f"Введите кол-во голды для вывода\n\nВаш баланс - {db_help.check_user(call.from_user.id)[4]} голды/{db_help.check_user(call.from_user.id)[3]} рублей")
    await UserState.vivod.set()

@dp.callback_query_handler(text="profile")
async def test(call: types.CallbackQuery):
    await call.message.edit_text(f"⚙️ Профиль\n\nID - {call.from_user.id}\nБаланс (рубли) - {db_help.check_user(call.from_user.id)[3]}\nБаланс (голда) - {db_help.check_user(call.from_user.id)[4]}\nРефералов - {db_help.check_user(call.from_user.id)[2]}", reply_markup=keyboards.profile())

@dp.callback_query_handler(text="support")
async def test(call: types.CallbackQuery):
    await call.message.edit_text(f"✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>", reply_markup=keyboards.supportMenu())


@dp.callback_query_handler(text="exit")
async def test(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())

@dp.message_handler(content_types=["photo"], state=UserState.screen)
async def golda(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.photo[-1].download("screen.jpg")
    photo = InputFile("screen.jpg")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="✅", callback_data=f"a_{message.from_user.id}"))
    await bot.send_photo(chat_id=adminid, photo=photo, caption= f'Вывод голды {data["golds"]} голды\n\nID Пользователя - {data["ids"]}', reply_markup=markup)
    await message.answer('Успешно!', reply_markup=keyboards.exitmenu())
    await state.finish()
@dp.callback_query_handler(text="otziiv")
async def test(call: types.CallbackQuery):
    await call.message.edit_text(f"Напишите текст отзыва", reply_markup=keyboards.exitmenu())
    await UserState.otziv.set()

@dp.callback_query_handler(text_startswith="a_")
async def test(call: types.CallbackQuery):
    ids = call.data.split('_')[1]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="Оставить отзыв", callback_data="otziiv"))

    await bot.send_message(ids, f"✅ Администратор подтвердил вывод голды. Оставьте отзыв нажав на кнопку ниже", reply_markup=markup)


@dp.callback_query_handler(text="golds")
async def test(call: types.CallbackQuery):
    pricegold = float(db_help.goldsc()[1])
    await call.message.edit_text(f"🥇 Курс голды на данный момент - {pricegold}", reply_markup=keyboards.exitmenu())


@dp.callback_query_handler(text="pay")
async def test(call: types.CallbackQuery):
    await call.message.edit_text(f"⚙️ Введите сумму пополнения", reply_markup=keyboards.exitmenu())
    await UserState.pay.set()


@dp.message_handler(state=UserState.otziv)
async def get_username(message: types.Message, state: FSMContext):
    await message.answer('Спасибо за отзыв!', reply_markup=keyboards.exitmenu())
    await message.forward(adminid, message)
    await state.finish()

@dp.message_handler(state=UserState.pay)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    async with QiwiP2PClient(
            secret_p2p="",#в кавычки вписать секретный киви p2p ключ купить можно @ms_shop_robot
            shim_server_url="http://play.nanix.fun:80/proxy/p2p/"
    ) as client:
        bill = await client.create_p2p_bill(amount=message.text)
        shim_url = client.create_shim_url(bill.invoice_uid)


    await state.finish()

    await state.set_state("payment")
    await state.update_data(bill=bill, summa=message.text)

    maiMenu = InlineKeyboardMarkup(row_wight=2)
    url = InlineKeyboardButton(text='QiWi', url=f'{shim_url}')
    chek = InlineKeyboardButton(text="Проверить оплату", callback_data="check")
    maiMenu.row(url, chek)

    await message.answer(text=f"Доступные платежные сервисы\n ", reply_markup=maiMenu)


@dp.callback_query_handler(state="payment", text="check")
async def handle_successful_payment(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: Bill = data.get("bill")
    print(bill.amount.value)
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        maiMenu = InlineKeyboardMarkup(row_wight=2)
        can = InlineKeyboardButton(text="❌", callback_data="exit")
        maiMenu.row(can)
        await call.message.edit_text("✅ Оплата прошла, средства зачисленны на ваш баланс.", reply_markup=maiMenu)
        await bot.send_message(adminid, f"✅ Пополнение. \nПополнил - {call.message.chat.id} на сумму {int(bill.amount.value)}")
        now = str(datetime.now())

        db_help.add_balance(int(bill.amount.value), call.message.chat.id)
        await state.finish()
    else:
        maiMenu = InlineKeyboardMarkup(row_wight=2)
        chek = InlineKeyboardButton(text="Проверить оплату", callback_data="check")
        can = InlineKeyboardButton(text="❌", callback_data="exit")
        maiMenu.row(can, chek)
        await call.message.edit_text("❌ Оплата не прошла, попробуйте еще раз.", reply_markup=maiMenu)
        await state.finish()


@dp.message_handler(state=UserState.suma)
async def get_username(message: types.Message, state: FSMContext):
    if message.text.isdigit() == True:
        pricegolda = float(db_help.goldsc()[1])
        balnce = float(message.text)//pricegolda
        if balnce >= 50:
            balnce = float(message.text)*pricegolda
            if db_help.check_user(message.from_user.id)[3] >= balnce:
                await state.finish()
                db_help.add_gold(message.from_user.id, message.text)
                db_help.del_balance(message.from_user.id, balnce)
                await bot.send_message(message.from_user.id, f"✅ <b>Вы купили {message.text} голды!</b>", reply_markup=keyboards.exitmenu())
                await bot.send_message(adminid, f"🔔 <b>{message.from_user.id} - {message.from_user.first_name} купил - {message.text} G по курсу - {float(db_help.goldsc()[1])}, на {balnce}</b>")
            else:
                await state.finish()
                await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно денег!</b>", reply_markup=keyboards.exitmenu())
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно денег!\n\nМинимальная сумма покупки - 50 рублей</b>", reply_markup=keyboards.exitmenu())
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, f"❗️ <b>Введите число!</b>", reply_markup=keyboards.exitmenu())

@dp.message_handler(state=UserState.vivod)
async def get_username(message: types.Message, state: FSMContext):
    if message.text.isdigit() == True:
        if int(db_help.check_user(message.from_user.id)[4]) >= int(message.text):
            if int(message.text) >= int(30):
                photo = InputFile("example.jpg")
                gold = float(message.text)+float(message.text)*float(0.25)
                db_help.del_gold(message.from_user.id, message.text)
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'Выставьте скин {skin} за {gold} голды, затем отправьте скриншот скина на рынке. (как в прикрепленном изображении)')
                await state.update_data(ids=message.from_user.id, golds=gold)
                await UserState.screen.set()
            else:
                await state.finish()

                await bot.send_message(message.from_user.id, f"❗️ <b>Минимальная сумма для вывода - 30 G!</b>", reply_markup=keyboards.exitmenu())

        else:
            await state.finish()
            await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно голды!</b>", reply_markup=keyboards.exitmenu())

    else:
        await state.finish()
        await bot.send_message(message.from_user.id, f"❗️ <b>Введите число!</b>", reply_markup=keyboards.exitmenu())



@dp.message_handler(commands=["db"])
async def command_start(message: types.Message):
    if message.from_user.id==admins:
        await bot.send_document(chat_id=admins, document = open('users.db', 'rb'), caption = f'🔔 BACKUP от {datetime.datetime.now()}')



@dp.message_handler(commands=["backup"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        await backup()
        await message.answer('Бекап система включена')

@dp.message_handler(commands=["give_rub"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        user, money = message.get_args().split()
        db_help.add_balance(user, money)
        await message.answer('Успешно')

@dp.message_handler(commands=["del_rub"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        user, money = message.get_args().split()
        db_help.del_balance(user, money)
        await message.answer('Успешно')

@dp.message_handler(commands=["dbg"])
async def command_start(message: types.Message):
    db_help.dbgolds()

@dp.message_handler(commands=["gold"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        cours = message.get_args().split()
        db_help.golds(cours)
        await message.answer(f'Успешно')

@dp.message_handler(commands=["give_gold"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        user, money = message.get_args().split()
        db_help.add_gold(user, money)
        await message.answer('Успешно')

@dp.message_handler(commands=["del_gold"])
async def command_start(message: types.Message):
    if message.from_user.id==adminid:
        user, money = message.get_args().split()
        db_help.del_gold(user, money)
        await message.answer('Успешно')



@dp.message_handler(commands=['alert'])
async def alert(message):
    try:
        if message.chat.id==adminid:
            await bot.send_message(message.chat.id, f"*Рассылка началась*", parse_mode='Markdown')
            receive_users, block_users = 0, 0
            spisok=func.spisok()
            for user1 in spisok:
                try:
                    await bot.send_message(user1[0], message.text[message.text.find(' '):])
                    receive_users += 1
                except:
                    block_users += 1
                await asyncio.sleep(0.4)
            await bot.send_message(message.chat.id, f"*Рассылка завершена *\n"
                                                    f"Сообщение получили: *{receive_users}*\n"
                                                    f"Сообщение не получили: *{block_users}*", parse_mode='Markdown')
    except Exception as e:
        print('Ошибка 1', e)

# ======

async def my_function():

    await bot.send_document(chat_id=adminid, document = open('users.db', 'rb'), caption = f'🔔 BACKUP от {datetime.datetime.now()}')

async def schedule_function():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            # Запуск функции в 12:00:00
            asyncio.ensure_future(my_function())
        await asyncio.sleep(1)

async def backup():
    asyncio.create_task(schedule_function())

def setup():
    "Setup function"

    print('[BOT] Started')
    executor.start_polling(dp)



# ======


if __name__ == "__main__":
    setup()
