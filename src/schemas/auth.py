from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class ReadUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
