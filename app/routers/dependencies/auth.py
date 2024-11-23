from hashlib import sha256
import hmac
from urllib.parse import parse_qsl

from app.schemas.telegram import TelegramAuthRequest

def verify_telegram_data(data: TelegramAuthRequest, bot_token: str) -> bool:
    """
    Проверка подписи данных, переданных Telegram.
    """
    
    auth_data = data.__dict__
    auth_data = {k: v for k, v in auth_data.items() if k != "hash"}
    sorted_data = sorted(auth_data.items())
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_data)
    secret_key = sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), sha256).hexdigest()
    return hmac_hash == auth_data.get("hash")