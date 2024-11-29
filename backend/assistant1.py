import os
import requests
from dotenv import load_dotenv



class YandexAssistant:
    def __init__(self):
        # Загрузка переменных окружения из .env файла
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        # Получение API-ключа
        self.api_key = os.getenv("YANDEX_API_KEY")
        if not self.api_key:
            raise ValueError("Yandex API Key not found. Please set it in the .env file.")

        # URL для API
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }

        # Загрузка системного промпта из файла
        self.system_prompt = self.load_system_prompt()

    def load_system_prompt(self):
        """
        Загружает системный промпт из файла prompts/assistant_prompt.txt.
        Если файл отсутствует, создаёт его с базовым содержимым.
        """
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "assistant_prompt.txt")
        if not os.path.exists(prompt_path):
            default_prompt = "You are a helpful assistant. Your role is to assist users with detailed and accurate responses."
            os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
            with open(prompt_path, "w", encoding="utf-8") as file:
                file.write(default_prompt)
            print(f"Файл {prompt_path} создан с содержимым по умолчанию.")
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def chat(self, user_prompt, temperature=0.2, max_tokens=400):
        """
        Отправляет запрос к Yandex Foundation Models для генерации текста.

        :param user_prompt: Строка с текстом запроса от пользователя
        :param temperature: Параметр креативности ответа (по умолчанию 0.7)
        :param max_tokens: Максимальное количество токенов в ответе (по умолчанию 200)
        :return: Сгенерированный текст ответа
        """
        data = {
            "modelUri": "gpt://yandexgpt/latest",  # Указание конкретной модели Яндекса
            "completionOptions": {
                "temperature": temperature,
                "maxTokens": max_tokens,
                "topP": 0.95
            },
            "messages": [
                {"role": "system", "text": self.system_prompt},
                {"role": "user", "text": user_prompt}
            ]
        }

        try:
            print("Отправляемые данные:", data)  # Отладочное сообщение
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()  # Проверка на успешность запроса
            result = response.json()
            print("Ответ API:", result)  # Отладочное сообщение
            return result.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "Нет текста в ответе")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API Яндекса: {e}")
            return "Извините, произошла ошибка при обработке запроса."
