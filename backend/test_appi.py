
import os
import requests
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
api_key = os.getenv("YANDEX_API_KEY")
# URL для тестового запроса
api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Заголовки запроса
headers = {
    "Authorization": f"Api-Key {api_key}",
    "Content-Type": "application/json",
}

# Данные запроса
data = {
    "modelUri": "gpt://yandexgpt/latest",
    "completionOptions": {
        "temperature": 0.7,
        "maxTokens": 200,
        "topP": 0.95
    },
    "messages": [
        {"role": "system", "text": "You are a helpful assistant."},
        {"role": "user", "text": "привет"}
    ]
}

# Убедитесь, что все строки в данных закодированы в UTF-8
for key, value in data.items():
    if isinstance(value, str):
        data[key] = value.encode('utf-8').decode('utf-8')
    elif isinstance(value, dict):
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, str):
                value[sub_key] = sub_value.encode('utf-8').decode('utf-8')

try:
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()  # Проверка на успешность запроса
    result = response.json()
    print("Ответ API:", result)  # Отладочное сообщение
    print("API-ключ действителен и имеет необходимые права доступа.")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к API Яндекса: {e}")
    print("Проверьте API-ключ и права доступа.")
