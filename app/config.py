import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


class Settings:
    RABBITMQ_HOST: str = "rabbitmq"  # Default to the RabbitMQ service name in Docker Compose
    RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
    SECRET_KEY = os.getenv("SECRET_KEY", "DbSLoIREJtu6z3CVnpTd_DdFeMMRoteCU0UjJcNreZI")
    PROJECT_NAME: str = "Address Service"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/address_service_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "Sylvian")
    DATABASE_DB: str = os.getenv("DATABASE_DB", "address_service_db")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5433"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    MAILGUN_API_KEY: str = os.getenv("MAILGUN_API_KEY", "e49cc11247477dcc0148736764d720c9-777a617d-74dfeb53")
    MAILGUN_SENDER_EMAIL: str = os.getenv("MAILGUN_SENDER_EMAIL", "fylinde.marketplace@gmail.com")
    MAILGUN_DOMAIN: str = os.getenv("MAILGUN_DOMAIN", "sandbox85bd3537b8ab41e6a2c8dd94469b05cc.mailgun.org")
    SECURITY_PASSWORD_SALT: str = os.getenv("SECURITY_PASSWORD_SALT", "mX-rk2vC6fyBmWPncH54sbHVLv4dT0FqQE2mysbkeKM")
    GMAIL_USER: str = os.getenv("GMAIL_USER", "fylinde.marketplace@gmail.com")
    GMAIL_PASSWORD: str = os.getenv("GMAIL_PASSWORD", "mmzm fpjh opgh aozk")
    ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY", "7f1416bb80db4d393fecdc929ea8d0f82992ed49ecb773cb147136d3184ba70f")
    HERE_MAPS_API_KEY: str = os.getenv("HERE_MAPS_API_KEY", "XeyqiLeQdoOHRl8aM6qxkG1vBYy-uYt-5fuyv7lMg7Y")
    HERE_APP_ID: str = os.getenv("HERE_APP_ID", "S5a03zsh66EnzLXgsns2")
settings = Settings()

