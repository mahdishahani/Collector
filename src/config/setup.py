import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # OpenAPI documentation.
    name: str = None
    version: str = None

    # Service parameters.
    service_name: str = None
    service_log_level: str = None

    debug: bool = None
    database_hostname: str = None
    database_port: int = None
    database_username: str = None
    database_password: str = None
    database_name: str = None
    rabbitmq_default_user: str = None
    rabbitmq_default_pass: str = None
    rabbitmq_default_vhost: str = None
    rabbitmq_default_host: str = None
    rabbitmq_default_port: str = None
    rabbit_url: str = None

    class Config:
        env_file = ".env"


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
