from dotenv import load_dotenv
import os
import logging

load_dotenv(dotenv_path=".env", override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        logger.error("SECRET_KEY missing in .env! Generate one with: `python -c 'import secrets; print(secrets.token_hex(24))'`")
        raise ValueError("SECRET_KEY must be set in .env")
    
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite3')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

logger.info("SECRET_KEY: %s", Config.SECRET_KEY)
logger.info("DATABASE_URI: %s", Config.SQLALCHEMY_DATABASE_URI)
