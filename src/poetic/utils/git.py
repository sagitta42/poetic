import os
from pathlib import Path
import subprocess
from typing import Callable

from poetic.logger import logg


class Git:
    """
    Git operations management.

    Simple management utilizing subprocess.
    """

    def __init__(self, path: Path | None) -> None:
        self.path = path or Path.cwd()

    @property
    def is_git_repo(self) -> bool:
        """
        Is current path a git repository.
        """
        return ".git" in os.listdir(self.path)

    def run(self, *args, check: bool = False) -> str | None:
        """
        Simple command run in template root directory.

        check (bool): check and return command output
        """
        action = self._get_command_output if check else self._run_command
        ret = action(*args)
        return ret

    def get_active_branch(self) -> str:
        """
        Get name of active branch.
        """
        check = self._get_command_output("rev-parse", "--abbrev-ref", "HEAD")
        ret = check.strip()
        return ret

    def branch_exists(self, branch_name: str) -> bool:
        branches = self.get_branch_list()
        ret = branch_name in branches
        return ret

    def commit_all(self, commit_message: str):
        """
        Add and commit all files.
        """
        self._run_command("add", "*")
        self._run_command("commit", "-am", commit_message)

    def get_last_commit(self) -> str:
        """
        Get hash of last commit.
        """
        output = self._get_command_list_output("rev-list", "HEAD")
        ret = output[0]
        return ret

    def get_first_commit(self) -> str:
        """
        Get hash of first commit.
        """
        output = self._get_command_list_output("rev-list", "HEAD")
        ret = output[-1]
        return ret

    def get_branch_list(self) -> list[str]:
        """
        Get list of branch names
        """
        output = self._get_command_list_output("branch", "--list")

        def clean_branch_name(name: str) -> str:
            ret = name
            if ret.startswith("*"):
                ret = ret[1:]
            ret = ret.strip()
            return ret

        ret = [clean_branch_name(branch) for branch in output]
        return ret

    def get_commit_message(self, commit: str) -> str:
        """
        Get commit message of given commit hash.
        """
        output = self._get_command_list_output("show", "--quiet", commit)
        ret = output[-1]
        return ret

    def _get_command_list_output(self, *args) -> list[str]:
        """
        Get command output in list form.

        Convert single string output into list.
        """
        output = self._get_command_output(*args)
        split_output = output.split("\n")
        ret = [out.strip() for out in split_output if not out == ""]
        return ret

    def _run_command(self, *args) -> None:
        self._run_subprocess(subprocess.run, *args)

    def _get_command_output(self, *args) -> str:
        ret = self._run_subprocess(subprocess.check_output, *args, text=True)
        return ret

    def _run_subprocess(self, subprocess_func: Callable, *args, **kwargs) -> str | None:
        logg.debug(args)
        ret = subprocess_func(["git"] + list(args), cwd=self.path, **kwargs)
        return ret
