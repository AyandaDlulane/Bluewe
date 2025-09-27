from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
import hashlib
import secrets
import jwt
import time
import re
from typing import Dict

from models import User, TokenResponse, VerifyResponse
import config

router = APIRouter()
security = HTTPBearer()
users_db: Dict[str, dict] = {}

def get_user_language(request: Request) -> str:
    accept_language = request.headers.get("accept-language", "en")
    if "es" in accept_language: return "es"
    elif "fr" in accept_language: return "fr"
    elif "zh" in accept_language: return "zh"
    elif "ar" in accept_language: return "ar"
    return "en"

def is_valid_username(username: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,20}$', username))

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex() + ":" + salt

def verify_password(password: str, hashed: str) -> bool:
    try:
        stored_hash, salt = hashed.split(":")
        new_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000
        ).hex()
        return stored_hash == new_hash
    except:
        return False

def create_token(username: str) -> str:
    payload = {
        "user": username, 
        "exp": time.time() + (config.TOKEN_EXPIRE_HOURS * 3600),
        "iat": time.time()
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return payload["user"]
    except:
        return None

@router.post("/register")
async def register(user: User, request: Request):
    lang = user.language or get_user_language(request)
    
    if not is_valid_username(user.username):
        raise HTTPException(400, "Username must be 3-20 characters (letters, numbers, _, -)")
    
    if len(user.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    
    if user.username in users_db:
        raise HTTPException(400, config.MESSAGES[lang]["user_exists"])
    
    users_db[user.username] = {
        "password_hash": hash_password(user.password),
        "language": lang,
        "created_at": time.time()
    }
    
    return {"message": config.MESSAGES[lang]["register_success"]}

@router.post("/login", response_model=TokenResponse)
async def login(user: User, request: Request):
    lang = user.language or get_user_language(request)
    
    if user.username not in users_db:
        raise HTTPException(400, config.MESSAGES[lang]["invalid_credentials"])
    
    user_data = users_db[user.username]
    
    if not verify_password(user.password, user_data["password_hash"]):
        raise HTTPException(400, config.MESSAGES[lang]["invalid_credentials"])
    
    token = create_token(user.username)
    return TokenResponse(
        token=token,
        user=user.username,
        language=user_data["language"],
        message=config.MESSAGES[lang]["login_success"]
    )

@router.get("/verify", response_model=VerifyResponse)
async def verify(token: str = Depends(security), request: Request = None):
    username = verify_token(token.credentials)
    if not username or username not in users_db:
        lang = get_user_language(request) if request else "en"
        raise HTTPException(401, config.MESSAGES[lang]["invalid_token"])
    
    user_data = users_db[username]
    return VerifyResponse(
        user=username,
        language=user_data["language"],
        valid=True,
        message=f"{config.MESSAGES[user_data['language']]['welcome']} {username}"
    )

@router.get("/users")
async def list_users():
    return {"users": list(users_db.keys())}