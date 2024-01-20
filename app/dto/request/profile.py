from datetime import date

from pydantic import BaseModel

from app.dto.request.auth import AccountType


class ChangePasswordRequestDto(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
    access_token: str

    def to_dict(self):
        return self.model_dump(exclude={'access_token'})


class AddRoleRequestDto(BaseModel):
    account_type: AccountType
    access_token: str


class UpdateUserRequestDto(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birthday: date | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    access_token: str

    def to_dict(self):
        d = self.model_dump(exclude={'access_token'})
        if self.birthday:
            d['birthday'] = self.birthday.isoformat()
        return d

class DeleteUserRequestDto(BaseModel):
    access_token: str
