import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def get_gsheet_client():
    """
    Создает и возвращает авторизованный клиент Google Sheets API.

    Returns:
        gspread.Client: Авторизованный клиент для работы с Google Sheets.
    """
    # Определяем область доступа для Google Sheets и Google Drive API
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Путь к credentials.json, который указан в .env
    credentials_path = os.getenv("GSHEET_CREDENTIALS_PATH")
    if not credentials_path:
        raise ValueError("GSHEET_CREDENTIALS_PATH не указан в файле .env")

    # Создаем учетные данные для доступа
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

    # Авторизация с использованием учетных данных
    client = gspread.authorize(creds)
    return client
