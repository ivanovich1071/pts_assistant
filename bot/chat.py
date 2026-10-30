from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from dotenv import load_dotenv

load_dotenv()

# Токен берётся из переменной окружения (см. .env.example)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Напишите любое сообщение, и я покажу ваш Chat ID.")

@dp.message_handler()
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Ваш Chat ID: {chat_id}")
    print(f"Chat ID: {chat_id}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
