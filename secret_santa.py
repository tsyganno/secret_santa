import logging
from random import choice
from os import getenv
import time
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

from db import Sql_lite
load_dotenv()

API_TOKEN = getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = Sql_lite()

people = ['Моника Белуччи', 'Корней Тарасов', 'Киану Ривз', 'Джейсон Стэтхем', 'Роберт Родригес']


def keyboard_secret_santa():
    """Создание кнопки HAPPY_NEW_YEAR"""
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_1 = types.KeyboardButton('/HAPPY_NEW_YEAR')
    keyboard.add(button_1)
    return keyboard


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет, я Тайный Санта =)\n'
                        'Для определения человека, которому тебе нужно будет подарить подарок, '
                        'нажми кнопку "HAPPY_NEW_YEAR"', reply_markup=keyboard_secret_santa())


@dp.message_handler(commands=['HAPPY_NEW_YEAR'])
async def echo(message: types.Message):
    try:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        user_name = message.from_user.username
        time_user = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        while True:
            name_of_person = choice(people)
            flag_name_person = db.search_name_in_database(name_of_person)
            if flag_name_person is False:
                break

        flag_write_in_db = db.search_id_user_in_database(us_id)
        if flag_write_in_db is False:
            db.write_to_the_database(
                id_user=us_id,
                first_name=us_name,
                last_name=us_sname,
                username=user_name,
                date=time_user,
                person_name=name_of_person,
            )
            await message.answer(f'Вы выбрали {name_of_person}', reply_markup=keyboard_secret_santa())
        else:
            await message.answer(f'Вы уже выбрали человека, которому будете дарить подарок.'
                                 f'\nЕго имя --- {flag_write_in_db}--- =)', reply_markup=keyboard_secret_santa())
    except:
        await message.answer('Нажми кнопку "HAPPY_NEW_YEAR" =)', reply_markup=keyboard_secret_santa())


@dp.message_handler()
async def send_welcome(message: types.Message):
    await message.answer('Нажми кнопку "HAPPY_NEW_YEAR" =)', reply_markup=keyboard_secret_santa())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
