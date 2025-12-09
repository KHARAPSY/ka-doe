from fastapi import HTTPException, status

from app.core import setup_logger, AuthPass
from app.db import PostgresConnect
from app.models import User
from app.schemas import UserInDB

class ServiceUser:
    _logger = setup_logger("User Services")

    @classmethod
    def create_user(cls, username: str, password: str, email: str, full_name: str, is_admin: bool = False):
        cls._logger.debug(f"Creating new user : `{username}`.")
        session = PostgresConnect.get_session()
        cls._logger.debug("Creating database session.")

        try:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                cls._logger.debug(f"User `{username}` already exist. Skipping creation.")
                return

            hashed_password = AuthPass.get_password_hash(password)

            new_user = User(
                username=username,
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                disabled=False,
                is_admin=is_admin
            )

            session.add(new_user)
            session.commit()

            cls._logger.debug(f"User `{username}` created successfully.")

        except Exception as e:
            session.rollback()
            cls._logger.exception(f"Error creating new user: {e}")
        finally:
            session.close()
            cls._logger.debug("Database connection closed.")

    @classmethod
    def get_user(cls, username: str) -> UserInDB | None:
        cls._logger.debug(f"Attempting to retrieve user : `{username}`.")
        session = PostgresConnect.get_session()
        cls._logger.debug("Creating database session.")

        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                cls._logger.debug(f"User `{username}` not found.")
                return None

            cls._logger.debug(f"User `{username}` successfully retrieved.")
            return UserInDB(
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
                is_admin=user.is_admin,
            )

        finally:
            session.close()
            cls._logger.debug("Database connection closed.")

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> UserInDB | None:
        cls._logger.debug(f"Authenticating user : `{username}`.")
        session = PostgresConnect.get_session()
        cls._logger.debug("Creating database session.")

        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                cls._logger.debug(f"Authentication failed: User `{username}` not found.")
                return None

            if not AuthPass.verify_password(password, user.hashed_password):
                cls._logger.debug(f"Authentication failed: Incorrect password for user `{username}`.")
                return None

            if user.disabled:
                cls._logger.debug(f"Authentication failed: User `{username}` is disabled.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is disabled"
                )

            return UserInDB(
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
                is_admin=user.is_admin,
            )

        finally:
            session.close()
            cls._logger.debug("Database connection closed.")
