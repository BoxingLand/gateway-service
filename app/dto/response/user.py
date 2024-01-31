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
