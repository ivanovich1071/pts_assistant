from utils import save_to_gsheets, save_to_telegram

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
