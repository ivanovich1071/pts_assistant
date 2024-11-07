from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Замените на ваш токен
TELEGRAM_BOT_TOKEN = '7379043295:AAH8pugKRcZ2SLydVV_Ek6duqjCLxPBU49A'

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
