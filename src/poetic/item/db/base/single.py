from pathlib import Path
from typing import Generic, Self

from poetic.item.db.base.base import BaseDBSetup
from poetic.item.env_settings import EnvSettingsSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.utils.db import DBEnvVars, T_DBEnvVars


class SingleDBSetup(BaseDBSetup, Generic[T_DBEnvVars]):
    """
    Single DB setup.

    dotenv_vars: DB environment variables in .env template
    """

    def __init__(
        self, path: Path, env_vars: T_DBEnvVars, settings: DBSettings, core: bool
    ) -> None:
        super().__init__(path, settings, core)

        self._env_vars = env_vars

        self._env_settings_setup = EnvSettingsSetup(
            self.path, template_setup=self._type, core=False
        )

    @property
    def main(self) -> Self:
        return self

    @property
    def dotenv_vars(self) -> DBEnvVars:
        """
        .env variables
        """
        return self._env_vars

    def setup(self) -> None:
        super().setup()

        self.setup_dotenv_template()

    def setup_dotenv_template(self):
        """
        Set up DB .env variables in .env.template.
        """
        super().setup_dotenv_template()

        self._add_env_vars()

    def setup_readme(self):
        """
        Set up README.

        Add DB readme.
        Add alembic readme.
        """
        super().setup_readme()

        logg.info("...setting up README.md")

        self._readme.add_new_section("DB", header=2)
        path_to_db_readme = self._templates.get_filepath(
            "README.md", subdir=self.db_type.value
        )
        self._readme.update_from_template(path_to_db_readme)

    def _add_env_vars(self, comment: bool = False):
        """
        Add env vars to .env template as values or commented out.
        """
        for env_var in self.dotenv_vars.set_vars:
            self._env.set(**env_var.model_dump(), comment=comment)
