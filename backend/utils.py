import requests
from auth import get_gsheet_client
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Получаем токен и ID чата из config.py или из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def save_to_gsheets(data):
    """
    Сохраняет данные в Google Sheets.

    Args:
        data (list): Список значений для добавления в Google Sheets, например, ["Имя", "Телефон"]

    Returns:
        str: Статус операции.
    """
    try:
        # Создаем клиент Google Sheets
        client = get_gsheet_client()

        # Открываем таблицу по ее ID
        spreadsheet_id = "your_spreadsheet_id_here"  # Замените на реальный ID вашей таблицы
        sheet = client.open_by_key(spreadsheet_id)

        # Открываем нужный лист по индексу (0 для первого листа) или имени
        worksheet = sheet.get_worksheet(0)

        # Добавляем данные в первую свободную строку
        worksheet.append_row(data)

        return "Данные успешно добавлены в Google Sheets."
    except Exception as e:
        print(f"Ошибка при добавлении данных в Google Sheets: {e}")
        return "Ошибка при добавлении данных в Google Sheets."


def save_to_telegram(name, phone):
    """
    Отправляет уведомление в Telegram с данными пользователя.

    Args:
        name (str): Имя пользователя.
        phone (str): Телефон пользователя.

    Returns:
        str: Статус отправки уведомления.
    """
    try:
        # Формируем URL для отправки сообщения через Telegram Bot API
        message = f"Новый пользователь оставил данные:\nИмя: {name}\nТелефон: {phone}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        # Данные для отправки
        payload = {
            "chat_id": "@your_telegram_channel_or_chat_id",  # Замените на ID чата
            "text": message
        }

        # Отправляем запрос
        response = requests.post(url, json=payload)

        # Проверяем успешность запроса
        if response.status_code == 200:
            return "Уведомление успешно отправлено в Telegram."
        else:
            print(f"Ошибка при отправке уведомления в Telegram: {response.text}")
            return "Ошибка при отправке уведомления в Telegram."
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "Ошибка при отправке уведомления в Telegram."
