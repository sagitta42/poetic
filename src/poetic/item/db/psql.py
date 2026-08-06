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
        return False
