import logging
from dotenv import dotenv_values


class Logger:
    def __init__(self, log_level=logging.INFO):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        self._logger.addHandler(handler)

    @property
    def info(self):
        return self._logger.info

    @property
    def error(self):
        return self._logger.error

    @property
    def debug(self):
        return self._logger.debug


env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
logg = Logger(log_level=logging.DEBUG if is_debug else logging.INFO)
