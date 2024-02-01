from datetime import datetime, date

from pydantic import BaseModel
from starlette.responses import StreamingResponse


class DeleteUserResponseDto(BaseModel):
    message: str


class UpdateUserResponseDto(BaseModel):
    message: str


class ChangePasswordResponseDto(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class AddRoleResponseDto(BaseModel):
    message: str


class UserBoxerProfileResponseDto(BaseModel):
    first_name: str
    last_name: str
    sex: str
    birthday: date
    country: str
    region: str
    weight: float
    height: float
    athletic_distinction: str
    avatar: str

class BoxerProfileResponseDto(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    club: str | None = None
    country: str | None = None
    region: str | None = None
    weight: float | None = None
    birthday: date
    athletic_distinction: str | None = None
    avatar: str
