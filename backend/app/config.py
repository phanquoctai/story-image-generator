from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_CREDENTIALS: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/story_generator"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Server
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "/tmp/uploads"
    OUTPUT_DIR: str = "/tmp/outputs"
    
    # Image Generation
    NUM_IMAGES_PER_STORY: int = 8
    IMAGE_QUALITY: str = "hd"
    IMAGE_SIZE: str = "1024x1024"
    
    # Story Generation
    STORY_SCENES: int = 8
    STORY_LANGUAGE: str = "vi"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()