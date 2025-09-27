from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    language: Optional[str] = "en"

class TokenResponse(BaseModel):
    token: str
    user: str
    language: str
    message: str

class VerifyResponse(BaseModel):
    user: str
    language: str
    valid: bool
    message: str
