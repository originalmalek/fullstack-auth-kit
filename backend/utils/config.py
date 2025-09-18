import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


class Settings:
    if os.getenv('MODE') == 'DEV':
        MONGODB_URL: str | None = os.getenv('MONGODB_TEST_URL')
        ROOT_URL: str | None = os.getenv('ROOT_TEST_URL')
    else:
        _raw_mongo_url = os.getenv('MONGODB_URL')
        _password = os.getenv('MONGODB_PASSWORD') or ''
        _encoded_pwd = quote_plus(_password)
        if _raw_mongo_url and '<PASSWORD>' in _raw_mongo_url:
            MONGODB_URL: str | None = _raw_mongo_url.replace('<PASSWORD>', _encoded_pwd)
        else:
            MONGODB_URL: str | None = _raw_mongo_url
        ROOT_URL: str | None = os.getenv('ROOT_URL')

    _database_name = os.getenv('MONGODB_NAME')
    if not _database_name:
        raise ValueError('MONGODB_NAME environment variable is required')
    DATABASE_NAME: str = _database_name

    # Security
    SECRET_KEY: str | None = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY: str | None = os.getenv('JWT_SECRET_KEY')

    # Email
    MAIL_CONSOLE: bool = os.getenv('MAIL_CONSOLE', 'false').lower() == 'true'
    MAIL_USERNAME: str | None = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str | None = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER: str | None = os.getenv('MAIL_SERVER')
    MAIL_FROM: str | None = os.getenv('MAIL_FROM')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 465))


settings = Settings()
