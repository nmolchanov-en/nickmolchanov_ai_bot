import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import openai
import os

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот-психолог Николая Молчановa. Задай мне вопрос по психологии и бизнесу.")

@dp.message_handler()
async def handle_message(message: types.Message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты бот-психолог, эксперт по когнитивным искажениям и маркетингу. Используй стиль Николая Молчанова."},
            {"role": "user", "content": message.text}
        ]
    )
    await message.reply(response.choices[0].message["content"])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
