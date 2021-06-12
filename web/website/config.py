import os


class Config:
    # File paths
    DATA_PATH = "data"
    ASSETS_PATH = "assets"

    PORT = os.environ.get('PORT')
    # Check whether supplied or not, else 5000
    PORT = PORT if PORT else 5000

    # Flask debug config (either True or False)
    debug_env = os.environ.get('DEBUG')
    # Check for True or False if env supplied, else True
    DEBUG = debug_env == '1' if debug_env else True

    # Database config
    DB_NAME = "user_history.db"
    secret_env = os.environ.get('SECRET_KEY')
    # Production config should supply the SECRET_KEY env variable
    SECRET_KEY = secret_env if secret_env else 'qjklsdsjkfu shjkghqyuez'

    if DEBUG:
        print("\n[INFO] USING DEBUG CONFIG\n")
        # use SQLite3 if in debug mode
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    else:
        print("\n[INFO] USING PRODUCTION CONFIG\n")
        # use PostgreSQL in production
        pg_user = os.environ.get('POSTGRES_USER')
        pg_pass = os.environ.get('POSTGRES_PASS')
        pg_db = os.environ.get('POSTGRES_DB')
        # This hostname must be same with the service name used in docker compose
        pg_host = 'db'
        pg_port = 5432

        SQLALCHEMY_DATABASE_URI = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
