import os
import requests
from dotenv import load_dotenv

# Загрузка .env файла
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Переменные из .env
oauth_token = os.getenv("YANDEX_OAUTH_TOKEN")  # Чтение OAuth-токена из .env

# URL для получения IAM-токена
iam_url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

# Путь к файлу для сохранения IAM-токена
file_path = os.path.join(os.path.expanduser("~"), "iam_token.txt")

# Функция для получения IAM-токена
def get_iam_token(oauth_token):
    try:
        # Проверка наличия OAuth-токена
        if not oauth_token:
            raise ValueError("OAuth-токен отсутствует. Укажите действительный OAuth-токен.")

        # Заголовки и тело запроса
        headers = {"Content-Type": "application/json"}
        data = {"yandexPassportOauthToken": oauth_token}

        # Выполнение POST-запроса
        response = requests.post(iam_url, headers=headers, json=data)
        response.raise_for_status()  # Проверяем успешность запроса

        # Извлечение IAM-токена из ответа
        iam_token = response.json().get("iamToken")
        if not iam_token:
            raise ValueError("Не удалось извлечь IAM-токен из ответа API.")

        print("IAM-токен успешно получен.")
        return iam_token
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except ValueError as ve:
        print(f"Ошибка: {ve}")
    return None

# Функция для сохранения IAM-токена в файл
def save_iam_token_to_file(iam_token, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(iam_token)
        print(f"IAM-токен успешно сохранён в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении IAM-токена: {e}")

# Основная логика
if __name__ == "__main__":
    # Получение IAM-токена
    iam_token = get_iam_token(oauth_token)
    if iam_token:
        save_iam_token_to_file(iam_token, file_path)
    else:
        print("Не удалось получить IAM-токен. Проверьте ошибки выше.")