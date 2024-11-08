import os
from dotenv import load_dotenv
import openai


class OpenAIChat:
    def __init__(self):
        # Загружаем переменные окружения
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)

        # Инициализируем параметры модели OpenAI
        self.model = "gpt-3.5-turbo"  # Замените на нужную модель
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

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
        Отправляет сообщение пользователя в OpenAI API и получает ответ.
        """
        prompt = self.load_prompt() + "\nUser: " + user_message + "\nAssistant:"

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
        except openai.error.OpenAIError as e:
            print(f"Ошибка при подключении к OpenAI API: {e}")
            return "Извините, возникла ошибка при обработке вашего запроса."

    def chat(self, user_message):
        """
        Основной метод для общения с ассистентом.
        """
        return self.get_response(user_message)
