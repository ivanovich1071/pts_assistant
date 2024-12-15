import requests
import time
import base64

# Ваш IAM-токен и Catalog ID
iam_token = "t1.9euelZrKx52Wzs6KjciOi8mJlpnIl-3rnpWal5mVzonMl8yNk4yPmMiJkcbl8_d7TARF-e8fIw4s_t3z9zt7AUX57x8jDiz-zef1656VmpidnZePx4qOl46MzcaUy5Sa7_zN5_XrnpWax5XJmZPOxo2ZzpSPk8nKipvv_cXrnpWamJ2dl4_Hio6XjozNxpTLlJo.U3pVNG0d7w6A4vyVOT40lOLEDLk3mbOuliM6xsvbwF_2FLWiJmt18NPSDLVgzOIZKZ5MOhAx7qg1Ib0U8N2ZAw"
catalog_id = "b1g35v6315951u23335m"

# URL для асинхронной генерации изображения
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

# Заголовки
headers = {
    "Authorization": f"Bearer {iam_token}",
    "Content-Type": "application/json"
}

# Данные для запроса
data = {
    "modelUri": f"art://{catalog_id}/yandex-art/latest",
    "generationOptions": {
        "seed": 1863,
        "aspectRatio": {
            "widthRatio": 2,
            "heightRatio": 1
        }
    },
    "messages": [
    {
        "weight": 1,
        "text": """Автономная система хранения одежды GARDEROBOT: электроприводной конвейер с ячейками для хранения и выдачи спецодежды и личных вещей. Эффективная организация хранения для вахтовиков и крупных объектов: экономия времени, автоматическое управление, точная идентификация, минимизация ошибок, гигиеничность и комфорт. Изображение: HD full wallpaper, четкий фокус, сложные детали, глубина кадра."""
    }
]
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    request_id = response.json()['id']
    print(f"Request ID: {request_id}")

    # Ожидание обработки изображения
    print("Ожидание обработки изображения...")
    time.sleep(10)  # Пауза для обработки

    # URL для получения результата по ID операции
    result_url = f"https://llm.api.cloud.yandex.net/operations/{request_id}"

    # Повторный GET-запрос для получения изображения
    result_response = requests.get(result_url, headers=headers)

    if result_response.status_code == 200:
        result_data = result_response.json()

        # Проверка статуса операции
        if result_data.get("done", False):
            print("Обработка завершена.")

            # Получение base64-кодированного изображения
            image_base64 = result_data['response']['image']
            image_data = base64.b64decode(image_base64)

            # Сохранение изображения в файл
            with open("image.jpeg", "wb") as file:
                file.write(image_data)
            print("Изображение успешно сохранено как image.jpeg")
        else:
            print("Обработка ещё не завершена. Повторите запрос позже.")
    else:
        print(f"Ошибка получения результата: {result_response.status_code} - {result_response.text}")
else:
    print(f"Ошибка при отправке запроса: {response.status_code} - {response.text}")
