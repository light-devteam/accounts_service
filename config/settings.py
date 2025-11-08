from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import RegistrationMode


class Settings(BaseSettings):
    POSTGRES_URL: str

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False
    REGISTRATION_MODE: RegistrationMode = RegistrationMode.ALLOW

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
