# HMAC-SHA256: подпись и проверка сообщений

REST API сервис для подписи и проверки целостности сообщений по алгоритму HMAC-SHA256.

## Ограничения

Это учебный проект. HMAC — симметричный MAC, не является юридически значимой электронной подписью. Нет шифрования, нет асимметричных ключей, один общий секрет.

## Требования

- Python 3.10+
- Зависимости: fastapi, uvicorn, httpx

## Установка

git clone <url>
cd hmac-python
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

## Конфигурация

Создать config.json в корне проекта. Секрет в base64. Пример: config.json.example.

## Генерация секрета

python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode())"

## Запуск

python main.py

## Примеры

Подписать:
curl -sS -X POST http://localhost:8080/sign -H 'Content-Type: application/json' -d '{"msg":"hello"}'

Проверить:
curl -sS -X POST http://localhost:8080/verify -H 'Content-Type: application/json' -d '{"msg":"hello","signature":"<подпись>"}'

## Тесты

pytest tests/ -v

## Ротация секрета

Сгенерировать новый ключ командой выше и вставить в config.json.
