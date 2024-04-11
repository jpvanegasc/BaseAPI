from dataclasses import dataclass, asdict

from pydantic_settings import BaseSettings


@dataclass
class FastAPIAppConfig:
    title: str

    def to_dict(self):
        return asdict(self)


class Settings(BaseSettings):
    SERVICE_NAME: str = "plm-api"

    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "database"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "plm_development"

    def database_url(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
