from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Neon Postgres connection string, e.g.
    # postgresql+psycopg2://user:password@ep-xxxx.neon.tech/keepsake?sslmode=require
    database_url: str = "postgresql+psycopg2://user:password@localhost/keepsake"

    jwt_secret: str = "change-me-in-.env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days, low-stakes personal app

    # Cloudflare R2 (S3-compatible)
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "keepsake-media"
    r2_public_url: str = ""  # e.g. https://media.yourdomain.com

    class Config:
        env_file = ".env"


settings = Settings()
