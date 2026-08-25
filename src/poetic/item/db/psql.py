from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.utils.docker import DockerHandler


# TODO: generalize .env.template util
class EnvVar(BaseModel):
    name: str = Field(description="Variable name")
    value: Any = Field(description="Variable value")
    docker: Optional[str] = Field(
        default=None,
        description="Variable name in docker-compose environment; defaults to name",
        exclude=True,
    )

    @property
    def docker_env_name(self) -> str:
        return self.docker or self.name

    @property
    def dollar(self) -> str:
        """
        Get ${var} string.
        """
        ret = f"${{{self.name}}}"
        return ret


class PsqlDBSetup(BaseDBSetup):
    """
    PSQL database setup.

    env_vars: environment variables in docker-compose
    dotenv_vars: .env variables = env_vars + port
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._service_name = "db"

        self._env_vars = [
            EnvVar(name="DB_HOST", value="localhost"),
            EnvVar(name="DB_NAME", value="db"),
            EnvVar(name="DB_USER", value="user"),
            EnvVar(name="DB_PASSWORD", value="changeme", docker="POSTGRES_PASSWORD"),
        ]

        self._port = EnvVar(name="DB_PORT", value=5432)

        self._dotenv_vars = self._env_vars + [self._port]

        self._docker = DockerHandler(self.path)

    def setup_dependencies(self):
        """
        Set up dependencies for PSQL functionality.

        psycopg[binary] is needed for alembic migrations.
        """
        super().setup_dependencies()

        self._poetry_add("psycopg[binary]")

    def setup_db(self):
        super().setup_db()

        self.setup_docker_compose()

    def setup_docker_compose(self):
        """
        Set up docker-compose with PSQL.

        Set up DB service in docker-compose.
        Set container name.
        Set up environment variables in service environment.
        Set up port.
        """
        logg.info("...setting up PSQL docker-compose", header=True)

        path_to_template = self._get_template_path("docker-compose.yml")
        self._docker.update_docker_compose_from_template(path_to_template)
        self._docker.update_service_container_name(
            self._service_name, f"db_{self._settings.db.value}"
        )
        self._update_service_env_vars()
        self._update_service_port()

    def setup_dotenv_template(self):
        """
        Set up PSQL variables in .env.template.
        """
        super().setup_dotenv_template()

        for env_var in self._dotenv_vars:
            self._update_env(**env_var.model_dump())

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
            env[env_var.docker_env_name] = env_var.dollar

        self._docker.write_docker_compose(yml_info)

    def _update_service_port(self):
        """
        Set/update db service ports.
        """
        yml_info = self._get_docker_compose()

        service = yml_info["services"][self._service_name]
        if "ports" not in service:
            service["ports"] = []
        ports = service["ports"]

        port_str = f"{self._port.dollar}:{self._port.value}"
        if len(ports) > 0:
            ports[0] = port_str
        else:
            ports.append(port_str)

        self._docker.write_docker_compose(yml_info)

    def _get_docker_compose(self) -> dict[str, Any]:
        """
        Get docker-compose with db service.

        If does not exist, set up empty "db" in dict.
        """
        ret = self._docker.get_docker_compose()

        services = ret["services"]

        if self._service_name not in services:
            services[self._service_name] = {}

        return ret
