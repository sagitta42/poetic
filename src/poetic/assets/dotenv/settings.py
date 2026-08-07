from typing import Any, Self

from pydantic import Field, model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_url: str | None = Field(default=None, description="Direct DB URL")
    db_name: str | None = Field(default=None, description="DB name")
    db_host: str | None = Field(default=None, description="DB host")
    db_port: int | None = Field(default=None, description="DB port")
    db_user: str | None = Field(default=None, description="DB username")
    db_password: str | None = Field(default=None, description="DB password")
    debug: bool = False

    @property
    def db_components(self) -> list[Any]:
        """
        Separate DB information components
        """
        ret = [
            self.db_name,
            self.db_host,
            self.db_port,
            self.db_user,
            self.db_password,
        ]
        return ret

    @property
    def has_all_db_components(self) -> bool:
        """
        Settings contain all separate DB components.
        """
        ret = all(var is not None for var in self.db_components)
        return ret

    @property
    def has_any_db_component(self) -> bool:
        """
        At least one of the separate DB components is present in settings.
        """
        ret = any(var is not None for var in self.db_components)
        return ret

    @property
    def has_db_info(self) -> bool:
        """
        Settings contain full DB info
        """
        ret = self.db_url is not None or self.has_all_db_components
        return ret

    @model_validator(mode="after")
    def check_url(self) -> Self:
        """
        Check for DB URL information conflicts.
        """
        if self.has_db_info:
            if self.db_url is not None and self.has_any_db_component:
                raise ValueError(
                    "Provide either direct DB URL or separate components, not both!"
                )

        return self


settings = Settings()
