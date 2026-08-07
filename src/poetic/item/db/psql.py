from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings


# TODO: generalize .env.template util
class EnvVar(BaseModel):
    var: str = Field(description="Variable name")
    value: Any = Field(description="Variable value")


class PsqlDBSetup(BaseDBSetup):
    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._service_name = "db"

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
        self._update_service_port()

    def setup_dotenv_template(self):
        """
        Set up PSQL variables in .env.template.
        """
        super().setup_dotenv_template()

        for env_var in self._dotenv_vars:
            self._update_env(**env_var.model_dump())

    # TODO: generalize docker compose util
    def _update_service_env_vars(self):
        """
        Set/update environment variables db service.

        Set environment variable to be picked up from .env.template
            with the same name i.e. ${VAR} format.
        """
        yml_info = self._get_docker_compose()

        service = yml_info["services"][self._service_name]
        if "environment" not in service:
            service["environment"] = {}
        env = service["environment"]

        for env_var in self._env_vars:
            env[env_var.var] = f"${{{env_var.var}}}"

        self._write_docker_compose(yml_info)

    def _update_service_port(self):
        """
        Set/update db service ports.
        """
        yml_info = self._get_docker_compose()

        service = yml_info["services"][self._service_name]
        if "ports" not in service:
            service["ports"] = []
        ports = service["ports"]

        port_str = f"${{{self._port.var}}}:{self._port.value}"
        if len(ports) > 0:
            ports[0] = port_str
        else:
            ports.append(port_str)

        # TODO: store docker compose in member, update, write at the end
        self._write_docker_compose(yml_info)

    def _get_docker_compose(
        self, path_to_docker_compose: Path | None = None
    ) -> dict[str, Any]:
        """
        Get docker-compose with db service.

        If does not exist, set up empty "db" in dict.
        """
        ret = super()._get_docker_compose(path_to_docker_compose)

        services = ret["services"]

        if self._service_name not in services:
            services[self._service_name] = {}

        return ret
