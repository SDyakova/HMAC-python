from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_sign_valid_message():
    response = client.post("/sign", json={"msg": "hello"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "signature" in data
    assert isinstance(data["signature"], str)
    assert "=" not in data["signature"]


def test_verify_valid_signature():
    response = client.post("/sign", json={"msg": "hello"})
    signature = response.json()["signature"]
    response = client.post(
        "/verify", json={"msg": "hello", "signature": signature}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ok": True}


def test_verify_wrong_message():
    response = client.post("/sign", json={"msg": "hello"})
    signature = response.json()["signature"]
    response = client.post(
        "/verify", json={"msg": "world", "signature": signature}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ok": False}


def test_verify_wrong_signature():
    response = client.post(
        "/verify", json={"msg": "hello", "signature": "!!!"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "invalid_signature_format"


def test_sign_empty_message():
    response = client.post("/sign", json={"msg": ""})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "invalid_msg"


def test_verify_empty_message():
    response = client.post("/verify", json={"msg": "", "signature": "dGVzdA"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "invalid_msg"


def test_sign_deterministic():
    resp1 = client.post("/sign", json={"msg": "hello"})
    resp2 = client.post("/sign", json={"msg": "hello"})
    assert resp1.json()["signature"] == resp2.json()["signature"]
