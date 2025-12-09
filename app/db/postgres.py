from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from app.models import Base
from app.core import setup_logger, Settings

class PostgresConnect:
    _logger = setup_logger("Postgres Connection")
    postgres_uri = Settings.POSTGRES_URI
    _engine = None
    _session = None

    @classmethod
    def _get_engine(cls):
        if cls._engine is None:
            cls._logger.debug(f"Connecting to Postgres")
            cls._engine = create_engine(
                cls.postgres_uri,
                echo_pool=True,
                max_overflow=10,
                pool_size=5,
                pool_recycle=300,
                pool_timeout=30,
            )
            return cls._engine
        return cls._engine
    
    @classmethod
    def _ensure_database(cls):
        engine = cls._get_engine()
        # Check if the database exists and create it if it doesn't
        if not database_exists(engine.url):
            create_database(engine.url)
            cls._logger.debug(f"Database '{engine.url.database}' created successfully.")
        else:
            cls._logger.debug(f"Database '{engine.url.database}' already exists.")

    @classmethod
    def get_session(cls):
        cls._ensure_database()
        engine = cls._get_engine()
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)
