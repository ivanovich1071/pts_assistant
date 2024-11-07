import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Токен Telegram-бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ID чата или канала в Telegram, куда будут отправляться уведомления
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ID таблицы Google Sheets для хранения данных (при необходимости)
GSHEET_ID = os.getenv("GSHEET_ID")
