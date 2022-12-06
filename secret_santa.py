import logging
import sqlite3
from os import getenv
import time
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
load_dotenv()


API_TOKEN = getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('lol')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)