from pathlib import Path
from typing import Any

import yaml


class DockerHandler:
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
        yml_info = self.get_docker_compose()
        services = yml_info["services"]

        if service_name not in services:
            raise ValueError(
                f"Service {services} not found under docker-compose services!"
            )

        service = services[service_name]
        service["container_name"] = container_name

        # TODO: store docker compose in member, update, write at the end
        self.write_docker_compose(yml_info)

    def update_docker_compose_from_template(self, path_to_template: Path):
        """
        Update given docker-compose .yml file with contents of given template.

        Default to docker-compose.yml in root of setup.
        Create file if does not exist yet.
        """
        yml_info = self.get_docker_compose()

        with open(path_to_template) as f:
            yml_template = yaml.safe_load(f)

        yml_info["services"] |= yml_template["services"]

        # TODO: store docker compose in member, update, write at the end
        self.write_docker_compose(yml_info)

    def get_docker_compose(self) -> dict[str, Any]:
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

    def write_docker_compose(self, yml_info: dict[str, Any]):
        # FIXME: improve duplication
        with open(self.docker_compose, "w") as f:
            yaml.dump(yml_info, f)
