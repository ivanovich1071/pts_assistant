import os
import requests
from dotenv import load_dotenv


class YandexAssistant:
    def __init__(self):
        # Загрузка переменных окружения из .env файла
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        # Получение API-ключа
        self.iam_token = os.getenv("YANDEX_IAM_TOKEN")
        if not self.iam_token:
            raise ValueError("IAM-токен не найден в .env файле. Укажите YANDEX_IAM_TOKEN.")

        # URL для API
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Authorization": f"Bearer {self.iam_token}",
            "Content-Type": "application/json",
        }

        # Загрузка системного промпта из файла
        self.system_prompt = self.load_system_prompt()
        self.dialogue_history = []  # Хранение истории диалога

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

    def chat(self, user_message, temperature=0.7, max_tokens=200):
        """
        Отправляет запрос к Yandex Foundation Models для генерации текста.

        :param user_message: Строка с текстом запроса от пользователя
        :param temperature: Параметр креативности ответа
        :param max_tokens: Максимальное количество токенов в ответе
        :return: Сгенерированный текст ответа
        """
        # Добавляем пользовательское сообщение в историю диалога
        self.dialogue_history.append({"role": "user", "text": user_message})

        # Создание сообщения для модели
        messages = [{"role": "system", "text": self.system_prompt}] + self.dialogue_history

        data = {
            "modelUri": "gpt://b1g35v6315951u23335m/yandexgpt-lite",  # Указание конкретной модели Яндекса
            "completionOptions": {
                "temperature": temperature,
                "maxTokens": max_tokens,
                "topP": 0.95
            },
            "messages": messages
        }

        try:
            print("Отправляемые данные:", data)  # Отладочное сообщение
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()  # Проверка на успешность запроса
            result = response.json()
            print("Ответ API:", result)  # Отладочное сообщение

            # Получаем ответ ассистента
            assistant_response = result.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "Нет текста в ответе")
            # Добавляем ответ ассистента в историю диалога
            self.dialogue_history.append({"role": "assistant", "text": assistant_response})
            return assistant_response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API Яндекса: {e}")
            return "Извините, произошла ошибка при обработке запроса."


# Для тестирования диалога
if __name__ == "__main__":
    assistant = YandexAssistant()
    print("Начните диалог с ассистентом. Для выхода введите 'exit'.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Диалог завершён.")
            break
        response = assistant.chat(user_input)
        print(f"Ассистент: {response}")
