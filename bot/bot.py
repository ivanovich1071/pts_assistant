from telegram import Bot
from config import TELEGRAM_BOT_TOKEN  # Импорт токена из config.py

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_notification_to_telegram(name, phone):
    """
    Отправляет уведомление в Telegram с именем и телефоном пользователя.

    Args:
        name (str): Имя пользователя.
        phone (str): Телефон пользователя.

    Returns:
        str: Статус отправки уведомления.
    """
    # Сообщение для отправки в Telegram
    message = f"Новый пользователь оставил данные:\nИмя: {name}\nТелефон: {phone}"

    try:
        # Укажите ID чата или канала, куда будут отправляться уведомления
        chat_id = "@your_telegram_channel_or_chat_id"  # Замените на ваш реальный chat_id

        # Отправляем сообщение в указанный чат
        bot.send_message(chat_id=chat_id, text=message)
        return "Уведомление успешно отправлено в Telegram."
    except Exception as e:
        print(f"Ошибка при отправке уведомления в Telegram: {e}")
        return "Ошибка при отправке уведомления в Telegram."
