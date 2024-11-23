import logging
from flask import Flask, request, jsonify
from assistant1 import YandexAssistant
from utils import save_to_gsheets, save_to_telegram
from flask_cors import CORS

# Настройка логирования
logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

app = Flask(__name__)
CORS(app)  # Для поддержки запросов с разных источников

assistant = YandexAssistant()

@app.route('/')
def home():
    app.logger.info("Главная страница загружена")
    return "Flask сервер работает"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    app.logger.debug(f"Получено сообщение от пользователя: {user_message}")

    if not user_message:
        app.logger.warning("Пустое сообщение от пользователя")
        return jsonify({"error": "No message provided"}), 400

    try:
        # Используем метод chat, а не generate_text
        response_text = assistant.chat(user_message)
        app.logger.debug(f"Ответ от ассистента: {response_text}")
        return jsonify({"response": response_text})
    except Exception as e:
        app.logger.error(f"Ошибка при обработке запроса: {e}")
        return jsonify({"response": "Извините, возникла ошибка. Пожалуйста, попробуйте снова."}), 500

if __name__ == '__main__':
    app.run(debug=True)
