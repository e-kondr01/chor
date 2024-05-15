from pydantic import BaseModel


class BearerResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str
