from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_password: SecretStr

    class Config:
        env_file = 'data/bot_token_db_pas.env'
        env_file_encoding = 'utf-8'


config = Settings()
