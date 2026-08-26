from pathlib import Path
from typing import Any


from poetic.item.db.base import DBSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.utils.docker import DBEnvVars, DockerComposeHandler, EnvVar


class PsqlDBSetup(DBSetup):
    """
    PSQL database setup.
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._service_name = "db"

        self._env_vars.name.service_name = "POSTGRES_DB"
        self._env_vars.host = EnvVar(name="DB_HOST", value="localhost")
        self._env_vars.user = EnvVar(
            name="DB_USER", value="user", service_name="POSTGRES_USER"
        )
        self._env_vars.password = EnvVar(
            name="DB_PASSWORD", value="changeme", service_name="POSTGRES_PASSWORD"
        )
        self._port = EnvVar(name="DB_PORT", value=5432)

        self._docker = DockerComposeHandler(self.path)

    @property
    def dotenv_vars(self) -> DBEnvVars:
        """
        .env variables

        Composed of environment variables + port.
        """
        ret = self.env_vars.model_copy()
        ret.port = self._port
        return ret

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

        path_to_template = self._templates.get_filepath("docker-compose.yml")
        self._docker.update_from_template(path_to_template)
        self._docker.update_service_container_name(
            self._service_name, f"db_{self._settings.db_type.value}"
        )
        self._docker.update_service_env_vars(
            self._service_name, self._env_vars.set_vars, user_service_var_names=True
        )
        self._update_service_port()

    def _update_service_port(self):
        """
        Set/update db service ports.
        """

        service = self._docker.get_service(
            self._service_name, create_if_not_present=True
        )

        if "ports" not in service:
            service["ports"] = []
        ports = service["ports"]

        port_str = f"{self._port.dollar}:{self._port.value}"
        if len(ports) > 0:
            ports[0] = port_str
        else:
            ports.append(port_str)

        self._docker.update_service(self._service_name, service)
