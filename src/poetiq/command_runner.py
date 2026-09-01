from pathlib import Path
import subprocess
from typing import Callable

from poetiq.logger import logg
from poetiq.utils.misc import list_as_args


class BaseCommandRunner:
    """
    Base class for running subprocess command lines.
    """

    def __init__(self, path: Path | None, command: str | None = None) -> None:
        self.path = path or Path.cwd()
        self._command = command

    def run(
        self, *args, check_output: bool = False, info: bool = False, **kwargs
    ) -> list[str] | None:
        """
        Simple command run in directory.

        check_output (bool): return command output with subprocess.check_output().
            NOTE: if running with checking output, it is not displayed in terminal
        info (bool): display green poetiq info
        """
        full_args = self._full_args(*args)
        if logg.is_debug:
            logg.debug(f"{self.path} $ {list_as_args(full_args)}")
        elif info:
            if isinstance(full_args[0], Path):
                full_args[0] = full_args[0].stem
            logg.info(f"(poetiq) {list_as_args(full_args)}", poetiq=True)

        command = self._get_command_list_output if check_output else self._run_command
        ret = command(*args, **kwargs)

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
        """
        All arguments including main command if any.

        Strip path to executable in command unless in debug mode.
        """
        ret = list(args)
        if self._command is not None:
            ret = [self._command] + ret
        return ret
