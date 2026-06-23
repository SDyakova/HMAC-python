import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.codec import decode_base64url, encode_base64url
from src.config import load_config
from src.constants import HMAC_SIZE
from src.hmac_service import HMACSigner, hmac_service
from src.models import SignRequest, VerifyRequest, VerifyResponse

logger = logging.getLogger(__name__)
router = APIRouter()

config = load_config()
MAX_MSG_SIZE = config["max_msg_size_bytes"]


@router.post("/sign")
async def sign(
    request: SignRequest,
    signer: Annotated[HMACSigner, Depends(hmac_service)],
):
    """Подписать сообщение."""
    if not request.msg:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="invalid_msg"
        )

    if len(request.msg.encode("utf-8")) > MAX_MSG_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail="payload_too_large",
        )

    logger.info(
        "Подпись сообщения длиной %d байт.", len(request.msg.encode("utf-8"))
    )

    try:
        sig_bytes = signer.sign(request.msg)
        signature = encode_base64url(sig_bytes)
        return {"signature": signature}
    except Exception as e:
        logger.error("Ошибка подписи: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="internal"
        )


@router.post("/verify")
async def verify(
    request: VerifyRequest,
    signer: Annotated[HMACSigner, Depends(hmac_service)],
):
    """Проверить подпись сообщения."""
    if not request.msg:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="invalid_msg"
        )

    if not request.signature:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="invalid_signature_format",
        )

    if len(request.msg.encode("utf-8")) > MAX_MSG_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail="payload_too_large",
        )

    logger.info(
        "Проверка подписи для сообщения длиной %d байт.",
        len(request.msg.encode("utf-8")),
    )

    try:
        sig_bytes = decode_base64url(request.signature)
        if len(sig_bytes) != HMAC_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="invalid_signature_format",
            )
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="invalid_signature_format",
        )

    try:
        ok = signer.verify(request.msg, sig_bytes)
        return VerifyResponse(ok=ok)
    except Exception as e:
        logger.error("Ошибка проверки подписи: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="internal"
        )
