import requests
import datetime
import jwt
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Данные сервисного аккаунта берутся из переменных окружения (см. .env.example).
# Приватный ключ НИКОГДА не хранится в коде.
service_account_id = os.getenv("YC_SERVICE_ACCOUNT_ID")
key_id = os.getenv("YC_KEY_ID")
private_key = os.getenv("YC_PRIVATE_KEY")

# URL для получения IAM-токена
iam_url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

# Генерация JWT
def generate_jwt():
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "aud": iam_url,
        "iss": service_account_id,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(hours=1)).timestamp())
    }
    token = jwt.encode(payload, private_key, algorithm="PS256", headers={"kid": key_id})
    print("Сгенерированный JWT:", token)
    return token

# Запрос IAM-токена
def get_iam_token():
    jwt_token = generate_jwt()
    print("Отправляем JWT:", jwt_token)
    response = requests.post(iam_url, json={"jwt": jwt_token})
    print("Ответ API:", response.text)
    response.raise_for_status()
    return response.json()["iamToken"]

# Основная логика
if __name__ == "__main__":
    try:
        iam_token = get_iam_token()
        with open("iam_token.txt", "w") as f:
            f.write(iam_token)
        print("IAM-токен успешно сохранён в iam_token.txt")
    except Exception as e:
        print("Ошибка при получении IAM-токена:", e)
