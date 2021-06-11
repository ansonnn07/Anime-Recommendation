import os


class Config:
    # File paths
    DATA_PATH = "data"
    ASSETS_PATH = "assets"

    # Flask debug config (either True or False)
    DEBUG = os.environ.get('DEBUG') == '1' or True

    # Database config
    DB_NAME = "user_history.db"
    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or b'S\xacb\x12\\a\xeb\xc8\xfc\x85E6B\x15g\xe1'

    # PostgreSQL config
    pg_user = os.environ.get('POSTGRES_USER') or 'admin'
    pg_pass = os.environ.get('POSTGRES_PASS') or 'admin'
    pg_db = os.environ.get('POSTGRES_DB') or 'anime'
    # This hostname must be same with the service name used in docker compose
    pg_host = 'db'
    pg_port = 5432

    if DEBUG == True:
        print("\n[INFO] USING DEBUG CONFIG\n")
        # use SQLite3 if in debug mode
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') \
            or f'sqlite:///{DB_NAME}'
    else:
        print("\n[INFO] USING PRODUCTION CONFIG\n")
        # use PostgreSQL in production
        SQLALCHEMY_DATABASE_URI = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
