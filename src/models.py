from dataclasses import dataclass


@dataclass(frozen=True)
class SignRequest:
    """Модель запроса для подписи сообщения."""

    msg: str


@dataclass(frozen=True)
class VerifyRequest:
    """Модель запроса для проверки подписи."""

    msg: str
    signature: str


@dataclass(frozen=True)
class VerifyResponse:
    """Модель ответа с результатом проверки."""

    ok: bool
