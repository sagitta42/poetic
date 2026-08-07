from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings


# TODO: generalize .env.template setup
class EnvVar(BaseModel):
    var: str = Field(description="Variable name")
    value: Any = Field(description="Variable value")


class PsqlDBSetup(BaseDBSetup):
    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._env_vars = [
            EnvVar(var="DB_NAME", value="changeme"),
            EnvVar(var="DB_USER", value="changeme"),
            EnvVar(var="DB_PASSWORD", value="changeme"),
        ]

        self._port = EnvVar(var="DB_PORT", value=5432)

        self._dotenv_vars = self._env_vars + [self._port]

    @property
    def db_url(self) -> str:
        return "changeme"

    def setup_db(self):
        super().setup_db()

        self.setup_docker_compose()

    def setup_docker_compose(self):
        """
        Set up docker-compose with PSQL.

        Set up DB service in docker-compose.
        Set up environment variables in service environment.
        TODO: Set up port.
        TODO: Set up DB URL in API service if exists.
        """
        logg.info("..setting up PSQL docker-compose", header=True)

        path_to_template = self._get_template_path("docker-compose.yml")
        self._update_docker_compose_from_template(path_to_template)
        self._update_service_env_vars()

    def setup_dotenv_template(self):
        """
        Set up PSQL variables in .env.template.
        """
        super().setup_dotenv_template()

        for env_var in self._dotenv_vars:
            self._update_env(**env_var.model_dump())

    def _update_service_env_vars(self, service_name: str = "db"):
        """
        Set/update environment variables for given service.

        Set environment variable to be picked up from .env.template
            with the same name i.e. ${VAR} format.
        """
        yml_info = self._get_docker_compose()

        services = yml_info["services"]

        if service_name not in services:
            services[service_name] = {}
        service = services[service_name]

        if "environment" not in service:
            service["environment"] = {}
        env = service["environment"]

        for env_var in self._env_vars:
            env[env_var.var] = f"${{{env_var.var}}}"

        self._write_docker_compose(yml_info)
