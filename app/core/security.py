import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from app.core.config import settings

# Оскільки ми не можемо гарантувати наявність bcrypt без встановлення, 
# використаємо надійний метод з hashlib + hmac для "соління" паролів.
def get_password_hash(password: str) -> str:
    # Використовуємо SECRET_KEY як сіль
    salt = settings.secret_key.encode()
    return hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None
    except jwt.PyJWTError:
        return None
