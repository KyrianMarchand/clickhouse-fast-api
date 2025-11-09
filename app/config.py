from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 8123
    clickhouse_user: str = "default"
    clickhouse_password: str = ""
    clickhouse_database: str = "default"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
