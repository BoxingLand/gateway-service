from datetime import date
from enum import Enum

from fastapi import UploadFile
from pydantic import BaseModel

from app.dto.request.auth import AccountType


class SexType(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ChangePasswordRequestDto(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str

    def to_dict(self):
        return self.model_dump()


class AddRoleRequestDto(BaseModel):
    account_type: AccountType


class UploadFileRequestDto(BaseModel):
    is_avatar: bool = False
    file: UploadFile


class UpdateUserRequestDto(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    sex: SexType | None = None
    birthday: date | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None

    def to_dict(self):
        d = self.model_dump()
        if self.birthday:
            d['birthday'] = self.birthday.isoformat()
        return d
