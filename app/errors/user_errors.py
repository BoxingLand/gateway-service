from typing import Any
from uuid import UUID

from fastapi import HTTPException
from starlette import status


class UserNotFoundError(HTTPException):
    def __init__(
        self,
        incoming_id: UUID | str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if incoming_id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the user with id {incoming_id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
            headers=headers,
        )

class UserEmailExistError(HTTPException):
    def __init__(
        self,
        email: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if email:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The email {email} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email already exists.",
            headers=headers,
        )

class UserPhoneNumberExistError(HTTPException):
    def __init__(
        self,
        phone_number: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if phone_number:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The phone number {phone_number} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The phone number exists.",
            headers=headers,
        )

class UserPasswordNotMatchError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
            headers=headers,
        )

class UserPasswordIsEasyError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords is easy.",
            headers=headers,
        )

class UserCreateError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User is not create.",
            headers=headers,
        )

class UserEmailNotFoundError(HTTPException):
    def __init__(
        self,
        email: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if email:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The email {email} not found.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The email not found.",
            headers=headers,
        )


class UserPhoneNumberNotFoundError(HTTPException):
    def __init__(
        self,
        phone_number: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if phone_number:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The phone number {phone_number} not found.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The phone number not found.",
            headers=headers,
        )

class UserValidateError(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login details.",
            headers=headers,
        )

class UserRoleExistError(HTTPException):
    def __init__(
        self,
        role: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if role:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The user already have role {role}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user already have role.",
            headers=headers,
        )
