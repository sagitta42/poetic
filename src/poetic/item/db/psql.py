from pathlib import Path

import yaml

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg


class PsqlDBSetup(BaseDBSetup):
    @property
    def db_url(self) -> str:
        return "changeme"

    def setup_db(self):
        super().setup_db()

        self.setup_docker_compose()

    def setup_docker_compose(self):
        """
        Set up PSQL service in docker-compose.
        """
        logg.info("..setting up PSQL docker-compose", header=True)

        filename = "docker-compose.yml"

        path_to_yml = self.path / filename
        path_to_template = self._get_template_path(filename)
        self._update_yml_from_template(path_to_yml, path_to_template)

    def setup_dotenv_template(self):
        """
        Set up PSQL variables in .env.template.

        Extract env variables from docker-compose template and set them to "changeme".
        """
        # TODO: redundancy with DB_URL
        super().setup_dotenv_template()

        filename = "docker-compose.yml"
        path_to_template = self._get_template_path(filename)
        env_variables = self._get_env_vars_from_docker_compose(path_to_template)

        for var in env_variables:
            self._update_env(var, "changeme")

    def _get_env_vars_from_docker_compose(
        self, path_to_docker_compose: Path
    ) -> list[str]:
        """
        Get environment variables from docker-compose.

        Extract variables under db service assuming ${VAR} format
        """

        with open(path_to_docker_compose) as f:
            yml_info = yaml.safe_load(f)

        service_name = "db"
        env_info = yml_info["services"][service_name]["environment"]
        ret = [value[2:-1] for value in env_info.values()]
        return ret
