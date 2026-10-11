from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_name: str = "SmartBursary API"
    secret_key: str = "CHANGE_THIS_SECRET_KEY_BEFORE_DEPLOYMENT"
    access_token_minutes: int = 300  # 5 hours session timeout
    
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
    smtp_host: str = os.getenv("SMTP_HOST", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "1025"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@smartbursary.com")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "SmartBursary System")
    email_enabled: bool = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
