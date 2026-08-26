from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field
import yaml


class EnvVar(BaseModel):
    name: str = Field(description="Variable name")
    value: Any = Field(description="Variable value")
    service_name: Optional[str] = Field(
        default=None,
        description="Variable name in service docker-compose environment; defaults to name",
        exclude=True,
    )

    @property
    def service_env_name(self) -> str:
        return self.service_name or self.name

    @property
    def dollar(self) -> str:
        """
        Get ${var} string.
        """
        ret = f"${{{self.name}}}"
        return ret


class DockerComposeHandler:
    """
    Handler for managing docker-compose.yml
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.docker_compose = self.path / "docker-compose.yml"

    def update_service_container_name(self, service_name: str, container_name: str):
        """
        Set/Update container name of given service.
        """
        service = self.get_service(service_name)
        service["container_name"] = container_name
        self.update_service(service_name, service)

    def update_from_template(self, path_to_template: Path):
        """
        Update given docker-compose .yml file with contents of given template.

        Default to docker-compose.yml in root of setup.
        Create file if does not exist yet.
        """
        yml_info = self._read()

        with open(path_to_template) as f:
            yml_template = yaml.safe_load(f)

        yml_info["services"] |= yml_template["services"]

        # TODO: store docker compose in member, update, write at the end
        self._write(yml_info)

    def update_service(self, service_name: str, service_dict: dict[str, Any]):
        """
        Update docker compose service with given dict.
        """
        yml_info = self._read()
        yml_info["services"][service_name] = service_dict
        # TODO: store docker compose in member, update, write at the end
        self._write(yml_info)

    def update_service_env_vars(
        self, service_name: str, env_vars: list[EnvVar], use_service_name: bool
    ):
        """
        Set/update environment variables db service.

        Set environment variable to be picked up from .env.template
            with the same name i.e. ${VAR} format.
        """
        service = self.get_service(service_name, create_if_not_present=True)

        if "environment" not in service:
            service["environment"] = {}
        env = service["environment"]

        for env_var in env_vars:
            var_name = env_var.service_env_name if use_service_name else env_var.name
            env[var_name] = env_var.dollar

        self.update_service(service_name, service)

    def add_items_to_service(self, service_name: str, items: dict[str, Any]):
        """
        Add given items to service.
        """
        service = self.get_service(service_name)
        service |= items
        self.update_service(service_name, service)

    def get_service(
        self, service_name: str, create_if_not_present: bool = False
    ) -> dict[str, Any]:
        """
        Get service info from docker-compose.
        """
        yml_info = self._read()
        services = yml_info["services"]

        if service_name not in services:
            if create_if_not_present:
                services[service_name] = {}
            else:
                raise ValueError(
                    f"Service {services} not found under docker-compose services!"
                )

        service = services[service_name]
        return service

    def _read(self) -> dict[str, Any]:
        """
        Get docker-compose from given path to .yml.

        If does not exist, set up empty "services" in dict.
        """

        yml_info = {}
        if self.docker_compose.exists():
            with open(self.docker_compose) as f:
                yml_info = yaml.safe_load(f)

        if "services" not in yml_info:
            yml_info["services"] = {}

        return yml_info

    def _write(self, yml_info: dict[str, Any]):
        # FIXME: improve duplication
        with open(self.docker_compose, "w") as f:
            yaml.dump(yml_info, f)
