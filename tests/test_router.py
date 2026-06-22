"""Tests for API routes"""

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_sign_valid_message():
    """Подпись валидного сообщения."""
    response = client.post("/sign", json={"msg": "hello"})
    assert response.status_code == 200
    data = response.json()
    assert "signature" in data
    assert isinstance(data["signature"], str)
    assert "=" not in data["signature"]


def test_verify_valid_signature():
    """Проверка верной подписи."""
    response = client.post("/sign", json={"msg": "hello"})
    signature = response.json()["signature"]

    response = client.post(
        "/verify",
        json={"msg": "hello", "signature": signature},
    )
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_verify_wrong_message():
    """Проверка с изменённым сообщением."""
    response = client.post("/sign", json={"msg": "hello"})
    signature = response.json()["signature"]

    response = client.post(
        "/verify",
        json={"msg": "world", "signature": signature},
    )
    assert response.status_code == 200
    assert response.json() == {"ok": False}


def test_verify_wrong_signature():
    """Проверка с неверной подписью."""
    response = client.post(
        "/verify",
        json={"msg": "hello", "signature": "!!!"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid_signature_format"


def test_sign_empty_message():
    """Пустое сообщение — ошибка 400."""
    response = client.post("/sign", json={"msg": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid_msg"


def test_verify_empty_message():
    """Пустое сообщение при проверке — ошибка 400."""
    response = client.post(
        "/verify",
        json={"msg": "", "signature": "dGVzdA"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid_msg"


def test_sign_deterministic():
    """Одинаковые сообщения дают одинаковую подпись."""
    resp1 = client.post("/sign", json={"msg": "hello"})
    resp2 = client.post("/sign", json={"msg": "hello"})
    assert resp1.json()["signature"] == resp2.json()["signature"]
