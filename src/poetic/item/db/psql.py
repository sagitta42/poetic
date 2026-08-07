import yaml

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg


class PsqlDBSetup(BaseDBSetup):
    @property
    def db_url(self) -> str:
        return "todo"

    def setup_db(self):
        self._setup_docker_compose()

    def _setup_docker_compose(self):
        """
        Set up PSQL service in docker-compose.
        """
        logg.info("..setting up docker-compose", header=True)

        filename = "docker-compose.yml"

        path_to_yml = self.path / filename
        path_to_template = self._get_template_path(filename)
        self._update_yml_from_template(path_to_yml, path_to_template)
