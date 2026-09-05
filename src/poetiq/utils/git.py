import os
from pathlib import Path
import subprocess

from poetiq.command_runner import BaseCommandRunner
from poetiq.exceptions import PoetiqException
from poetiq.logger import logg


class Git(BaseCommandRunner):
    """
    Git operations management.

    Simple management utilizing subprocess.
    """

    def __init__(self, path: Path | None) -> None:
        super().__init__(path, command="git")

    @property
    def is_git_repo(self) -> bool:
        """
        Is current path a git repository.
        """
        return ".git" in os.listdir(self.path)

    @property
    def has_uncommitted_changes(self) -> bool:
        output = self.run("diff", check_output=True)
        logg.debug(output)
        ret = len(output) > 0
        return ret

    def get_active_branch(self) -> str:
        """
        Get name of active branch.
        """
        output = self.run("rev-parse", "--abbrev-ref", "HEAD", check_output=True)
        ret = output[0]
        return ret

    def branch_exists(self, branch_name: str) -> bool:
        branches = self.get_branch_list()
        ret = branch_name in branches
        return ret

    def commit_all(self, commit_message: str):
        """
        Add and commit all files.
        """
        self.run("add", "*")
        self.run("commit", "-am", commit_message, info=True)

    def get_last_commit(self) -> str:
        """
        Get hash of last commit.
        """
        output = self.run("rev-list", "HEAD", check_output=True)
        ret = output[0]
        return ret

    def get_first_commit(self) -> str:
        """
        Get hash of first commit.
        """
        output = self.run("rev-list", "HEAD", check_output=True)
        ret = output[-1]
        return ret

    def get_branch_list(self) -> list[str]:
        """
        Get list of branch names
        """
        output = self.run("branch", "--list", check_output=True)

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
        output = self.run("show", "--quiet", commit, check_output=True)
        ret = output[-1]
        return ret

    def run(self, *args, check_output: bool = False, info: bool = False, **kwargs) -> list[str] | None:
        try:
            return super().run(*args, check_output=check_output, info=info, **kwargs)
        except subprocess.CalledProcessError as e:
            command_display = self._get_command_display(*args, detailed=False)
            raise PoetiqException(f"poetiq failed running git command:\n$ {command_display}\nPlease handle and try again")