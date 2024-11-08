import os
from dotenv import load_dotenv
import openai

class OpenAIChat:
    def __init__(self):
        # Загружаем переменные окружения из файла .env
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        # Получаем ключ API
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key not found. Please set it in the .env file.")

        # Устанавливаем ключ API для openai
        openai.api_key = self.api_key
        self.model = "text-davinci-003"  # Замените на доступную модель, например, text-davinci-003

    def chat(self, message):
        try:
            # Используем Completion.create для стандартного текста
            response = openai.Completion.create(
                model=self.model,
                prompt=message,
                max_tokens=100
            )
            # Возвращаем текст из ответа
            return response.choices[0].text.strip() if response.choices else None
        except Exception as e:
            print("Ошибка при обращении к OpenAI API:", e)
            return None

# Функция для тестирования взаимодействия с OpenAI API
def test_openai_chat():
    # Создаем экземпляр OpenAIChat
    chat_assistant = OpenAIChat()

    # Пробное сообщение
    test_message = "Привет! Как тебя зовут?"

    # Получаем ответ от API
    response = chat_assistant.chat(test_message)

    # Выводим ответ или сообщение об ошибке
    if response:
        print("Ответ от OpenAI API:")
        print(response)
    else:
        print("Не удалось получить ответ от OpenAI API.")

# Запуск теста при запуске файла напрямую
if __name__ == "__main__":
    test_openai_chat()
