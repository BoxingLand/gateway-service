from pydantic import BaseModel


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
