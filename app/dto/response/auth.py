from pydantic import BaseModel


class SigninResponseDto(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class SignupResponseDto(BaseModel):
    message: str


class RefreshResponseDto(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
