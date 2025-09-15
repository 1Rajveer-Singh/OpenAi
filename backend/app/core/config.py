"""
Configuration settings for VyapaarGPT application
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from loguru import logger

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application settings
    app_name: str = "VyapaarGPT"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    encryption_key: Optional[str] = None
    password_salt: str = "vyapaargpt_salt"
    
    # Database settings
    database_url: Optional[str] = None
    async_database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "vyapaargpt"
    db_user: str = "postgres"
    db_password: str = "password"
    
    # OpenAI settings
    openai_api_key: str = "your-openai-api-key"
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.7
    
    # Voice settings
    whisper_model: str = "whisper-1"
    voice_languages: List[str] = [
        "hi", "te", "ta", "bn", "gu", "mr", "kn", "en"
    ]
    
    # External API settings
    whatsapp_business_token: Optional[str] = None
    whatsapp_phone_number_id: Optional[str] = None
    whatsapp_webhook_verify_token: Optional[str] = None
    
    razorpay_key_id: Optional[str] = None
    razorpay_key_secret: Optional[str] = None
    
    # ONDC (Open Network for Digital Commerce) settings
    ondc_gateway_url: str = "https://buyer-app-preprod-v2.ondc.org"
    ondc_subscriber_id: Optional[str] = None
    ondc_subscriber_key: Optional[str] = None
    
    # Marketplace API keys
    flipkart_api_key: Optional[str] = None
    flipkart_api_secret: Optional[str] = None
    
    amazon_access_key: Optional[str] = None
    amazon_secret_key: Optional[str] = None
    amazon_marketplace_id: Optional[str] = None
    
    meesho_api_key: Optional[str] = None
    
    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "vyapaargpt.log"
    log_max_size: str = "10 MB"
    log_retention: str = "7 days"
    
    # Business settings for India
    default_currency: str = "INR"
    default_timezone: str = "Asia/Kolkata"
    default_language: str = "hindi"
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf", "text/plain", "text/csv"
    ]
    
    # AI agent settings
    max_conversation_history: int = 20
    agent_response_timeout: int = 30
    enable_voice_responses: bool = True
    
    # Business insights settings
    enable_analytics: bool = True
    analytics_retention_days: int = 90
    
    # Compliance settings (for Indian regulations)
    enable_data_encryption: bool = True
    audit_log_retention_days: int = 365 * 3  # 3 years
    customer_data_retention_days: int = 365 * 7  # 7 years
    
    @validator("debug", pre=True)
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("voice_languages", pre=True)
    def parse_voice_languages(cls, v):
        if isinstance(v, str):
            return [lang.strip() for lang in v.split(",")]
        return v
    
    @validator("cors_allow_methods", pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v
    
    @validator("cors_allow_headers", pre=True)
    def parse_cors_headers(cls, v):
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v
    
    @validator("allowed_file_types", pre=True)
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    def get_database_url(self) -> str:
        """Get complete database URL"""
        if self.database_url:
            return self.database_url
        
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def get_async_database_url(self) -> str:
        """Get async database URL"""
        if self.async_database_url:
            return self.async_database_url
        
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def validate_required_apis(self) -> List[str]:
        """Validate that required API keys are present"""
        
        missing_apis = []
        
        if not self.openai_api_key or self.openai_api_key == "your-openai-api-key":
            missing_apis.append("OpenAI API Key")
        
        # Optional but recommended APIs
        warnings = []
        
        if not self.whatsapp_business_token:
            warnings.append("WhatsApp Business API not configured")
        
        if not self.razorpay_key_id:
            warnings.append("Razorpay payment gateway not configured")
        
        if not self.ondc_subscriber_id:
            warnings.append("ONDC marketplace integration not configured")
        
        if warnings:
            logger.warning("Optional integrations not configured: " + ", ".join(warnings))
        
        return missing_apis
    
    def get_language_config(self) -> dict:
        """Get language configuration for AI responses"""
        
        return {
            "supported_languages": self.voice_languages,
            "default_language": self.default_language,
            "language_names": {
                "hi": "हिन्दी (Hindi)",
                "te": "తెలుగు (Telugu)", 
                "ta": "தமிழ் (Tamil)",
                "bn": "বাংলা (Bengali)",
                "gu": "ગુજરાતી (Gujarati)",
                "mr": "मराठी (Marathi)",
                "kn": "ಕನ್ನಡ (Kannada)",
                "en": "English"
            }
        }
    
    def get_business_config(self) -> dict:
        """Get business-specific configuration for India"""
        
        return {
            "currency": self.default_currency,
            "timezone": self.default_timezone,
            "country": "IN",
            "business_types": [
                "retail", "wholesale", "manufacturing", "services", 
                "restaurant", "grocery", "electronics", "clothing",
                "pharmacy", "automotive", "real_estate", "education",
                "healthcare", "finance", "technology", "other"
            ],
            "payment_methods": [
                "cash", "upi", "card", "net_banking", "wallet", "cod"
            ],
            "tax_types": ["GST", "VAT", "Service Tax"],
            "units_of_measure": [
                "piece", "kg", "gram", "liter", "meter", "square_feet",
                "dozen", "packet", "box", "bundle"
            ]
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Validate required settings on startup
missing_apis = settings.validate_required_apis()
if missing_apis:
    logger.error(f"Missing required API configurations: {', '.join(missing_apis)}")
    logger.error("Please set the required environment variables before starting the application")

# Log current configuration (without sensitive data)
logger.info(f"VyapaarGPT {settings.app_version} starting up")
logger.info(f"Debug mode: {settings.debug}")
logger.info(f"Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
logger.info(f"Supported languages: {', '.join(settings.voice_languages)}")
logger.info(f"Default language: {settings.default_language}")
logger.info(f"Analytics enabled: {settings.enable_analytics}")
logger.info(f"Data encryption enabled: {settings.enable_data_encryption}")

# Environment-specific configurations
if settings.debug:
    logger.warning("Running in DEBUG mode - not suitable for production")
    
if settings.secret_key == "your-secret-key-change-in-production":
    logger.warning("Using default secret key - change this in production!")

# Export commonly used settings
DATABASE_URL = settings.get_database_url()
ASYNC_DATABASE_URL = settings.get_async_database_url()
LANGUAGE_CONFIG = settings.get_language_config()
BUSINESS_CONFIG = settings.get_business_config()