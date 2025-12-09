import os
from datetime import timedelta

def env(key, default=None):
    return os.environ.get(key, default)

class Settings:
    # Security
    SECRET_KEY = env("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    ENCODE = "utf-8"

    # Admin user
    ADMIN_USER = env("ADMIN_USER", "admin")
    ADMIN_PASS = env("ADMIN_PASS", "pass")
    ADMIN_EMAIL = env("ADMIN_EMAIL", "admin@example.com")
    ADMIN_NAME = env("ADMIN_NAME", "Super Admin")
    IS_ADMIN = True
    
    # PostgreSQL
    POSTGRES_URI = env("KADOE_POSTGRES_URI")
    if not POSTGRES_URI:
        postgres_host = env("KADOE_POSTGRES_HOST", env("DBS_SERVER_HOST")) or "localhost"
        POSTGRES_URI = (
            f"postgresql+psycopg2://{env('KADOE_POSTGRES_USER', 'user')}:"
            f"{env('KADOE_POSTGRES_PASS', 'password')}@{postgres_host}:"
            f"{env('KADOE_POSTGRES_PORT', '5432')}/{env('KADOE_POSTGRES_DB', 'ka_doe_db')}"
        )
    DATABASE_URL = POSTGRES_URI

    # MinIO
    MINIO_URI = env("KADOE_MINIO_URI")
    if not MINIO_URI:
        minio_host = env("KADOE_MINIO_HOST", env("DBS_SERVER_HOST")) or "localhost"
        MINIO_URI = f"http://{minio_host}:{env('KADOE_MINIO_PORT', '9000')}"
    MINIO_ENDPOINT = MINIO_URI
    MINIO_ACCESS_KEY = env("KADOE_MINIO_USER", "minioadmin")
    MINIO_SECRET_KEY = env("KADOE_MINIO_PASS", "minioadmin")
    MINIO_BUCKET_NAME = "my-knowledges"
    MINIO_FOLDER_DATA = "data-files/"
    MINIO_FOLDER_STOR = "content_storage/"

    # MongoDB
    MONGO_URI = env("KADOE_MONGO_URI")
    if not MONGO_URI:
        mongo_host = env("KADOE_MONGO_HOST", env("DBS_SERVER_HOST")) or "localhost"
        MONGO_URI = (
            f"mongodb://{env('KADOE_MONGO_USER', 'user')}:"
            f"{env('KADOE_MONGO_PASSWORD', 'password')}@{mongo_host}:"
            f"{env('KADOE_MONGO_PORT', '27017')}/{env('KADOE_MONGO_DB', 'ka_doe_db')}"
        )
