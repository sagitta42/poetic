from pathlib import Path
import subprocess
from typing import Callable

from poetic.logger import logg
from poetic.utils.misc import list_as_args


class BaseCommandRunner:
    """
    Base class for running subprocess command lines.
    """

    def __init__(self, path: Path | None) -> None:
        self.path = path or Path.cwd()
        self._main_command: str | None = None

    def run(self, *args, check: bool = False, **kwargs) -> list[str] | None:
        """
        Simple command run in directory.

        check (bool): check and return command output
        """
        action = self._get_command_list_output if check else self._run_command
        ret = action(*args, **kwargs)

        return ret

    def _get_command_list_output(self, *args, **kwargs) -> list[str]:
        """
        Get command output in list form.

        Convert single string output into list.
        """
        output = self._get_command_output(*args, **kwargs)
        split_output = output.split("\n")
        ret = [out.strip() for out in split_output if not out == ""]
        return ret

    def _run_command(self, *args, **kwargs) -> None:
        self._run_subprocess(subprocess.run, *args, **kwargs)

    def _get_command_output(self, *args, **kwargs) -> str | None:
        ret = self._run_subprocess(subprocess.check_output, *args, **kwargs, text=True)
        return ret

    def _run_subprocess(self, subprocess_func: Callable, *args, **kwargs) -> str | None:
        subprocess_args = list(args)
        if self._main_command is not None:
            subprocess_args = [self._main_command] + subprocess_args

        logg.debug(f"{self.path} $ {list_as_args(subprocess_args)}")

        ret = subprocess_func(subprocess_args, cwd=self.path, **kwargs)
        return ret
