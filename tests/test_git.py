from poetic.utils.git import Git

from poetic.logger import logg


def test_active_branch():
    git = Git()

    active_branch = git.get_active_branch()
    logg.info(f"Active branch: {active_branch}")


def test_branch_exists():
    git = Git()

    check = git.branch_exists("main")
    assert check


def test_first_commit():
    git = Git()

    first_commit = git.get_first_commit()

    assert first_commit == "44aeefafcb3af5c8591ae70cff11147afd1268f2"


def test_last_commit_message():
    git = Git()

    last_commit = git.get_last_commit()
    last_commit_message = git.get_commit_message(last_commit)

    logg.info(f"Last commit message: {last_commit_message}")
