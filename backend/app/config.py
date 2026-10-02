from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SmartBursary API"
    secret_key: str = "CHANGE_THIS_SECRET_KEY_BEFORE_DEPLOYMENT"
    access_token_minutes: int = 60
    database_url: str = "sqlite:///./smartbursary.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    upload_dir: str = "uploads"
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
