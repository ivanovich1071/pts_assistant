import requests
import datetime
import jwt

# Данные из ключа
service_account_id = "ajehfj1v3h3rlspg7vn9"  # ID сервисного аккаунта
key_id = "aje8j6fl19rf1kpl65ud"  # ID ключа
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCWSkj55bafyA9I
VMLdYCG3ScnMcc5okvmlliSIaZzVF5xIT+4oHgAGTo9n/RNXUzeCiiHjVZ0Lxt1d
Cbf++jBhqcShZt9I1uR3/zaTPbT7SJsoZJKU+lPB5m2UKBYrLThaQRSzdJ0pHM7T
OWCiZ0rZP1TN1FBuvRcm2nWbLYNGzZAYVYp0F02reobahgBnmicNAdPiyEjqcY9G
uRImKiiAsZWyIRaZ2lrYZxZ8Kv3RKwGq4SYMqEb128luthhhkqKRiZruSYyIlsoQ
ZG4U5vYVn3SWbh4frYN5y6TpHQbYpwXk8iVkNk7iJ8DPIzbIcScaJgVIVhFYfKyE
nlGJ7hMRAgMBAAECggEACVaEQkKrnjHoAS6DDQ40ChdjmnhXwtee+1Lg4jjtra/R
3gxZV9TFW571+hgXY42gHVRH1sAzCdBJYMaB0C3rY6YQuZaSuQvhFjOdSHjFDffs
7A2Trf3/xkRy+omjFvuwTKtOhffw6+UGVMlz36NbWzQ8KK3QcZD+J0PbmtCxH2z9
7EfRQfEIitk66rGkaWpsDyuh8Go2h03Xzem9FbfiabigZWGrA6Hxa6h3y2xCXHLy
JYTgUZB4ujaWsyrlP4V47TAh6uER0BcE6Xse26HLVQOkNopY09Qv+TZIStsvpbwA
JC+kJ0IB+5J1s43xD/u315SYzRc8LA1TIchseSFMoQKBgQC+ZkVveqeLSs5OJ804
BeLm3bn9jPPyWSlQGjaOpRX8BPPuMZKJSMmM/X3QCiYrWwyFq46WGskJGObAzPLV
TYdvdpqPTUKA6zHO2/q82afrhmZyWgSY3a3beoGBvfhOGMsKJrHTFuuai0M3Vpiv
yHYJIRDUc9vbVxNHYa6nshoVrwKBgQDKEkSRDmqS20fFx48YKHQDux6GnX1lDr5+
z97eEZ14U9Ei2XLddHaVrQY6ogwAsCCVnlCvun+Jo6oJhwGZ76kYyOMH60af6UmB
9oxf1RtlqvMFnpPOzYCsr+8CZ8gFpHiIjnwmnWBA0FObs6jqtsDJRUBrkZVKa3B8
1MGAgPVTPwKBgCIAsbXO+czudxmOEiBHLNZ+EpEtcwN82NvtUoD3Co4PdGC9iaXq
0dPUEXvt1BM6F2pn0PcNoYl2YP9dmqBtUBqf28prycysNCD1ODoxxMNTJUiWuutx
63Ke1jINcyK/WsNdVbSVC052QHLJjEsYSbwno5HNfx4U1uSQlVhtfisRAoGBAJ8d
VVp3ZJnxCwoEwnt+VyQc8sODPZsWyg+m9VIdwsZeEZ8EZLtWmo3vaak/sn3UMkQ+
HkDRdN3XvuuzoCIrohY/EO5KaBlBJD2u+wf3EZSz0JsLLE46aWkRO/3D5K/0u2ij
8cSiRYmjwUIobQktEI8r9bb+MvUftrrE+P2MDiEXAoGBAL1WmIzGd6snj9PUjTvh
D4hMXviJq18hLfTcqbtY1RE81QCx+pS3vF28AiI8KJp6cNIMjkQ1QJaaTAHptoU/
fNy7v3eMpt5A61pvymFbOUz97beatqo71Tq8zs/J39mmvyQ7bEp+ucuSACDeQ8S/
x1lIm4NlggfKnUJHUREqB/Mz
-----END PRIVATE KEY-----"""

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
