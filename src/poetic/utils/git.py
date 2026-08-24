import os
from pathlib import Path

from poetic.command_runner import BaseCommandRunner


class Git(BaseCommandRunner):
    """
    Git operations management.

    Simple management utilizing subprocess.
    """

    def __init__(self, path: Path | None) -> None:
        super().__init__(path)

        self._main_command = "git"

    @property
    def is_git_repo(self) -> bool:
        """
        Is current path a git repository.
        """
        return ".git" in os.listdir(self.path)

    def get_active_branch(self) -> str:
        """
        Get name of active branch.
        """
        output = self.run("rev-parse", "--abbrev-ref", "HEAD", check=True)
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
        self.run("commit", "-am", commit_message)

    def get_last_commit(self) -> str:
        """
        Get hash of last commit.
        """
        output = self.run("rev-list", "HEAD", check=True)
        ret = output[0]
        return ret

    def get_first_commit(self) -> str:
        """
        Get hash of first commit.
        """
        output = self.run("rev-list", "HEAD", check=True)
        ret = output[-1]
        return ret

    def get_branch_list(self) -> list[str]:
        """
        Get list of branch names
        """
        output = self.run("branch", "--list", check=True)

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
        output = self.run("show", "--quiet", commit, check=True)
        ret = output[-1]
        return ret
