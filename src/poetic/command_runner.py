from pathlib import Path
import subprocess
from typing import Callable

from poetic.logger import logg
from poetic.utils.misc import list_as_args


class BaseCommandRunner:
    """
    Base class for running subprocess command lines.
    """

    def __init__(self, path: Path | None, command: str | None = None) -> None:
        self.path = path or Path.cwd()
        self._command = command

    def run(self, *args, info: bool = False, **kwargs) -> list[str] | None:
        """
        Simple command run in directory.

        check (bool): check and return command output
        """
        full_args = self._full_args(*args)
        if info:
            logg.info(f"poetic: {list_as_args(full_args)}", green=True)
        else:
            logg.debug(f"{self.path} $ {list_as_args(full_args)}")

        ret = self._get_command_list_output(*args, **kwargs)

        return ret

    def _get_command_list_output(self, *args, **kwargs) -> list[str] | None:
        """
        Get command output in list form.

        Convert single string output into list.
        """
        output = self._get_command_output(*args, **kwargs)

        if output is None:
            return None

        split_output = output.split("\n")
        ret = [out.strip() for out in split_output if not out == ""]
        return ret

    def _get_command_output(self, *args, **kwargs) -> str | None:
        ret = self._run_subprocess(subprocess.check_output, *args, **kwargs, text=True)
        return ret

    def _run_command(self, *args, **kwargs) -> None:
        self._run_subprocess(subprocess.run, *args, **kwargs)

    def _run_subprocess(self, subprocess_func: Callable, *args, **kwargs) -> str | None:
        ret = subprocess_func(self._full_args(*args), cwd=self.path, **kwargs)
        return ret

    def _full_args(self, *args) -> list[str]:
        ret = list(args)
        if self._command is not None:
            ret = [self._command] + ret
        return ret
