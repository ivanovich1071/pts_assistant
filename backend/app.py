import logging
from flask import Flask, request, jsonify
from assistant import OpenAIChat
from utils import save_to_gsheets, save_to_telegram
from flask_cors import CORS
# Настройка логирования
logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

assistant = OpenAIChat()

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
        # Получаем ответ от ассистента
        response_text = assistant.chat(user_message)
        app.logger.debug(f"Ответ от ассистента: {response_text}")
        return jsonify({"response": response_text})
    except Exception as e:
        app.logger.error(f"Ошибка при обработке запроса: {e}")
        return jsonify({"response": "Извините, возникла ошибка. Пожалуйста, попробуйте снова."}), 500

def create_lead(name, phone):
    """
    Создает лид, записывая данные в Google Sheets и отправляя уведомление в Telegram.
    """
    # Сохранение данных в Google Sheets
    gsheet_status = save_to_gsheets([name, phone])

    # Отправка уведомления в Telegram
    telegram_status = save_to_telegram(name, phone)

    return {
        "gsheet_status": gsheet_status,
        "telegram_status": telegram_status
    }

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    app.logger.debug(f"Получены данные пользователя: имя={name}, телефон={phone}")

    if not name or not phone:
        app.logger.warning("Не указаны имя или телефон")
        return jsonify({"error": "Name and phone are required"}), 400

    try:
        lead_status = create_lead(name, phone)
        app.logger.debug(f"Статус лида: {lead_status}")
        return jsonify(lead_status)
    except Exception as e:
        app.logger.error(f"Ошибка при создании лида: {e}")
        return jsonify({"error": "Произошла ошибка при сохранении данных."}), 500

if __name__ == '__main__':
    app.run(debug=True)
