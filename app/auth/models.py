from pydantic import BaseModel


class AuthStartResponse(BaseModel):
    state: str


class AuthItemResponse(BaseModel):
    item: int
