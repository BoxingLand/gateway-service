from typing import Any

from fastapi import HTTPException
from starlette import status


class TokenExpiredSignatureError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your token has expired. Please log in again.",
            headers=headers,
        )


class TokenDecodeError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error when decoding the token. Please check your request.",
            headers=headers,
        )


class TokenMissingRequiredClaimError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is no required field in your token. Please contact the administrator.",
            headers=headers,
        )


class TokenIncorrectError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect token.",
            headers=headers,
        )