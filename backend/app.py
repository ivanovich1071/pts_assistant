from flask import Flask, request, jsonify
from assistant import MistralChat  # Импорт класса для общения с Mistral
from utils import save_to_gsheets, save_to_telegram  # Функции для сохранения данных
import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

app = Flask(__name__)
assistant = MistralChat()

@app.route('/')
def home():
    return "Flask сервер работает"

@app.route('/chat', methods=['POST'])
def chat():
    """Эндпоинт для общения с AI-ассистентом."""
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Получаем ответ от ассистента
    response_text = assistant.chat(user_message)
    return jsonify({"response": response_text})

@app.route('/submit_data', methods=['POST'])
def submit_data():
    """Эндпоинт для записи данных пользователя и отправки уведомления."""
    data = request.json
    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    # Сохраняем данные в Google Sheets
    gsheet_status = save_to_gsheets([name, phone])

    # Отправляем уведомление в Telegram
    telegram_status = save_to_telegram(name, phone)

    return jsonify({
        "gsheet_status": gsheet_status,
        "telegram_status": telegram_status
    })

if __name__ == '__main__':
    app.run(debug=True)

