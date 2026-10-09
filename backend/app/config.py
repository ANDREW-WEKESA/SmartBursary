from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_name: str = "SmartBursary API"
    secret_key: str = "CHANGE_THIS_SECRET_KEY_BEFORE_DEPLOYMENT"
    access_token_minutes: int = 60
    
    # Database - Railway provides DATABASE_URL automatically for PostgreSQL
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./smartbursary.db")
    
    # CORS - supports both local and production domains
    # Add your Vercel domain here: https://your-app.vercel.app
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
    )
    
    upload_dir: str = "uploads"
    max_upload_mb: int = 5
    
    # Email settings
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "noreply@smartbursary.com"
    smtp_from_name: str = "SmartBursary System"
    email_enabled: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
