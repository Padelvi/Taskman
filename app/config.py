from pydantic import BaseSettings

class DBSettings(BaseSettings):
    database_host: str
    database_port: str
    database_password: str
    database: str
    database_username: str

    class Config:
        env_file = ".env"

db_settings = DBSettings()
