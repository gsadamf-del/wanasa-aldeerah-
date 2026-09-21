from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://wanasa:wanasa@localhost:5432/wanasa"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: str = "*"
    payment_webhook_secret: str = "change-me-webhook"
    platform_commission_percent: float = 10.0
    environment: str = "development"
    rate_limit_requests: int = 120
    rate_limit_window_seconds: int = 60
    worker_name: str = "wanasa-outbox-worker"
    payment_provider: str = "mock"
    stripe_secret_key: str = ""
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_sandbox: bool = True
    fcm_project_id: str = ""
    fcm_access_token: str = ""
    apns_team_id: str = ""
    apns_key_id: str = ""
    apns_private_key: str = ""
    apns_bundle_id: str = "com.wanasa.aldeerah"
    apns_production: bool = False
    external_monitoring_url: str = ""
    external_monitoring_api_key: str = ""
    restore_drill_required: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
