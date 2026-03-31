import os
import hashlib
import hmac
import base64
import json
import time
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "voicecare-secret-key-change-in-production")

def hash_password(password: str) -> str:
    import hashlib, os
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, hash_val = hashed.split(":")
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == hash_val
    except:
        return False

def create_token(data: dict, expires_hours: int = 24) -> str:
    payload = {**data, "exp": time.time() + expires_hours * 3600}
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"

def verify_token(token: str) -> dict | None:
    try:
        payload_b64, sig = token.rsplit(".", 1)
        expected_sig = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except:
        return None