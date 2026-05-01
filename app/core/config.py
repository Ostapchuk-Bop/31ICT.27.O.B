from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:changeme@localhost/lab4_db"
    postgres_user: str = "postgres"
    postgres_password: str = "changeme"
    postgres_db: str = "lab4_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    class Config:
        env_file = ".env"


settings = Settings()