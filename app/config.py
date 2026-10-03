import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    # Codifica a palavra-passe para suportar caracteres especiais como @, !, #, etc.
    raw_password = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_PASSWORD = quote_plus(raw_password)
    
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "english_cards_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao_desenvolvimento")