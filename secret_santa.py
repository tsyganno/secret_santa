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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_1 = types.KeyboardButton('/s')
    keyboard.add(button_1)
    await message.reply('Привет, я Тайный Санта =)', reply_markup=keyboard)


@dp.message_handler(commands=['s'])
async def echo(message: types.Message):
    try:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        user_name = message.from_user.username
        time_user = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        name_of_person = choice(people)
        db.write_to_the_database(
            id_user=us_id,
            first_name=us_name,
            last_name=us_sname,
            username=user_name,
            date=time_user,
            person_name=name_of_person,
        )
        await message.answer(f'Вы выбрали {name_of_person}')
    except:
        await message.answer('СОБАКА')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
