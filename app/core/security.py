from passlib.context import CryptContext

# Настройка контекста для хэширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    
    :param password: Пароль в виде строки.
    :return: Захэшированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли пароль его хэшу.
    
    :param plain_password: Обычный пароль.
    :param hashed_password: Захэшированный пароль.
    :return: True, если пароль соответствует хэшу, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)
