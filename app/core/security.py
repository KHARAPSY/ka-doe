from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta, timezone
from jwt import encode, decode
from jwt.exceptions import InvalidTokenError

from .config import Settings
from .logger import setup_logger

class AuthToken:
    _logger = setup_logger("Authentication Token")

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        cls._logger.debug("Creating access token")

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        
        cls._logger.debug("Token expiration time set to: %s ", expire)
        try:
            token = encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
            cls._logger.debug("Token successfully encoded.")
            return token
        except Exception as e:
            cls._logger.exception("Failed to encode token: %s", e)
            raise

    @classmethod
    def decode_access_token(cls, token: str) -> dict | None:
        cls._logger.debug("Decoding token")

        try:
            decoded = decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
            cls._logger.debug("Token successfully decoded")
            return decoded
        except InvalidTokenError:
            cls._logger.warning("Invalid token provided.")
            return None
        except Exception as e:
            cls._logger.exception("Unexpected error while decoding token: %s", e)
            return None

class AuthPass:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return hashpw(password.encode(Settings.ENCODE), gensalt()).decode(Settings.ENCODE)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode(Settings.ENCODE), hashed_password.encode(Settings.ENCODE))

