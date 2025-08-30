from pydantic_settings import BaseSettings
from pydantic import ConfigDict, computed_field


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()  # type: ignore
