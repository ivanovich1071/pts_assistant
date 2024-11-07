import os
from dotenv import load_dotenv
import requests


class MistralChat:
    def __init__(self):
        # Загрузка переменных окружения
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        # Параметры для модели и API
        self.model = "mistral-large-latest"  # Имя модели Mistral
        self.api_key = os.getenv("MISTRAL_API_KEY")  # API-ключ Mistral из .env
        self.api_url = "https://api.mistral.com/generate"  # URL Mistral API (проверьте актуальность)
        self.timeout_limit = 20  # Таймаут в секундах для ожидания ответа от модели

    def load_prompt(self, filename="prompts/assistant_prompt.txt"):
        """
        Загружает промт из файла.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                prompt = file.read()
            return prompt
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Убедитесь, что путь к файлу указан правильно.")
            return ""

    def get_response(self, user_message):
        """
        Отправляет сообщение пользователя в Mistral и получает ответ.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Формируем полный промт с учетом начального текста и сообщения пользователя
        prompt = self.load_prompt()
        data = {
            "model": self.model,
            "prompt": prompt + "\nUser: " + user_message + "\nAssistant:",
            "max_tokens": 150,
            "temperature": 0.7,
            "stop": ["User:", "Assistant:"]
        }

        try:
            # Запрос к Mistral API с таймаутом
            response = requests.post(self.api_url, headers=headers, json=data, timeout=self.timeout_limit)
            response_data = response.json()

            if response.status_code == 200:
                return response_data.get("choices", [{}])[0].get("text", "").strip()
            else:
                print("Ошибка от Mistral API:", response_data)
                return "Извините, возникла ошибка при обработке вашего запроса."
        except requests.Timeout:
            return "Извините, запрос занял слишком много времени. Пожалуйста, попробуйте снова."
        except requests.RequestException as e:
            print(f"Произошла ошибка: {e}")
            return "Извините, возникла ошибка при подключении к сервису."

    def chat(self, user_message):
        """
        Основной метод для общения с ассистентом.
        """
        return self.get_response(user_message)
