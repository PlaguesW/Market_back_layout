from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "marketplace"
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    class Config:
        env_file = ".env"

settings = Settings()