from pathlib import Path

from poetic.item.db.base.docker import DockerDBSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings, DBType
from poetic.utils.db import ServiceDBEnvVars


class MongoDBSetup(DockerDBSetup[ServiceDBEnvVars]):
    def __init__(
        self,
        path: Path,
        env_vars: ServiceDBEnvVars,
        settings: DBSettings = DBSettings(db_type=DBType.mongo),
        core: bool = False,
    ) -> None:
        super().__init__(path, env_vars, settings, core)

    def setup_db(self):
        super().setup_db()

        logg.info("Here will be MongoDB setup", poetic=True)

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pymongo")

    def setup_readme(self):
        self._readme.add_new_section("MongoDB", header=3)
        super().setup_readme()