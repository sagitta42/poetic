import enum
import logging
from dotenv import dotenv_values


class AnsiStyle(str, enum.Enum):
    normal = "0"
    bold = "1"
    start = "\033["
    end = "\033[0m"

    def __str__(self) -> str:
        return self.value


class AnsiColor(str, enum.Enum):
    green = "32"
    grey = "90"
    red = "31"
    yellow = "33"
    white = "37"

    def apply(self, message: str | int, bold: bool = False) -> str:
        """
        To be used with color based
        """
        style = AnsiStyle.bold if bold else AnsiStyle.normal
        ret = f"{AnsiStyle.start}{style};{self.value}m{message}{AnsiStyle.end}"
        return ret

    def bold(self, message: str | int | float) -> str:
        """
        Shortcut for bold colored text
        """
        ret = self.apply(message, bold=True)
        return ret

    def __str__(self) -> str:
        return self.value


class Logger:
    def __init__(self, log_level=logging.INFO):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        self._logger.addHandler(handler)

    def info(self, message: str, header: bool = False):
        color = AnsiColor.green if header else AnsiColor.white
        return self._logger.info(color.apply(message, header))

    def error(self, message: str):
        return self._logger.error(AnsiColor.red.apply(message))

    def warning(self, message: str, important: bool = False):
        if important:
            message = f"! WARNING ! {message}"
        return self._logger.warning(AnsiColor.yellow.apply(message, important))

    def debug(self, message: str):
        return self._logger.debug(AnsiColor.grey.apply(message))


env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
logg = Logger(log_level=logging.DEBUG if is_debug else logging.INFO)
