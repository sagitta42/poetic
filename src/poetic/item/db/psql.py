import yaml

from poetic.item.db.base import BaseDBSetup
from poetic.logger import logg


class PsqlDBSetup(BaseDBSetup):
    @property
    def db_url(self) -> str:
        return "todo"

    def setup_db(self) -> bool:
        existed = self._setup_docker_compose()
        return existed

    def _setup_docker_compose(self) -> bool:
        logg.info("..setting up docker-compose", header=True)
        existed = False

        path_to_yml = self.path / "docker-compose.yml"

        yml_info = {}
        if path_to_yml.exists():
            existed = True
            with open(path_to_yml) as f:
                yml_info = yaml.safe_load(f)
        else:
            self._copy_template("docker-compose.yml")
            return False

        if "services" not in yml_info:
            yml_info["serices"] = {}

        db_yml_template = self._get_template_path(
            "docker-compose.yml", generic=False, template_subdir=None
        )
        with open(db_yml_template) as f:
            db_yml_info = yaml.safe_load(f)

        yml_info["services"]["db"] = db_yml_info["services"]["db"]

        with open(path_to_yml, "w") as f:
            yaml.dump(yml_info, f)

        return existed
