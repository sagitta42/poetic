from abc import abstractmethod
import os
from pathlib import Path
from typing import TypeVar

from poetic.exceptions import PoeticException
from poetic.setup.base import BaseSetup
from poetic.logger import logg
from poetic.settings import BaseTemplateSettings
from poetic.setup.settings import SettingsSetup
from poetic.utils.tree import tree

T_TemplateSettings = TypeVar("T_TemplateSettings", bound=BaseTemplateSettings)


class BaseTemplate(BaseSetup[T_TemplateSettings]):
    """
    General template setup.

    Includes
        - repository init (git, poetry)
        - repository setup
        - repository update

    Repository setup (in addition to BaseSetup):
        - gitignore
        - source files
        - VSCode
        - README
        - extra

    Repository update: updating existing template with poetic updates.

    """

    def __init__(self, settings: T_TemplateSettings) -> None:
        self.name = settings.name
        super().__init__(settings, Path(self.name))

        self._inner_name = self.name.replace("-", "_")

        # self._git_auto = Git(self._path_to_resources.parent.parent)

        self._poetic_link = "[poetic](https://github.com/sagitta42/poetic)"

        self._dotenv_settings: SettingsSetup | None = None

        logg.info(f"Setting up {self._type}: {self.name}")

    def init(self):
        """
        Initial setup of the template.

        Initialize package with poetry.
        Initialize git repository.
        Set up files.
        Make initial commit.
        Perform post-commit setup.
        """
        self.poetry_init()
        self.git.run("init")

        self.setup()

        self.git.commit_all(f"template made with {self._poetic_link}")

        self.post_init_commit()

        self.display()

    def update(self):
        """
        (Safe) Update existing template.

        Attempt an update, switch to original branch in case of fail.
        """
        current_branch = self.git.get_active_branch()
        logg.info(f"Active branch: {current_branch}")

        try:
            self._update(current_branch)
        except Exception as e:
            self.git.run("switch", current_branch)
            raise e

    def _update(self, current_branch: str):
        """
        Update existing template.

        Switch to branch dev-poetic-update.
            If does not exist, create starting from first repo commit.
            NOTE: assumes the first commit is the poetic template commit.
            NOTE: this branch is expected to be reserved for poetic updates.
        Run setup.
        Commit updates.
        Switch to current branch.
        Merge dev-poetic-update.
        """
        update_branch = "dev-poetic-update"
        if not self.git.branch_exists(update_branch):
            first_commit = self.git.get_first_commit()
            logg.info(
                f"Creating {update_branch} starting from first commit {first_commit}"
            )
            self.git.run("branch", update_branch, first_commit)

        self.git.run("switch", update_branch)

        self.setup()

        # FIXME: correctly get poetic commits
        # last_poetic_commit = self._git_auto.get_last_commit()
        # last_poetic_commit_message = self._git_auto.get_commit_message(
        # last_poetic_commit
        # )
        # message = f"{self._poetic_link} update\ncommit: {last_poetic_commit}\nmessage: {last_poetic_commit_message}"

        message = f"updated with {self._poetic_link}"
        self.git.commit_all(message)

        self.git.run("switch", current_branch)
        self.git.run("merge", update_branch)

    def setup(self, skip_super: bool = False) -> None:
        super().setup(skip_super)

        self.setup_gitignore()
        self.setup_source_files()
        if self._dotenv_settings is not None:
            self._dotenv_settings.setup(skip_super=True)
        self.setup_vscode()
        self.setup_readme()

    def setup_dependencies(self):
        self._poetry_add("dotenv")
        self._poetry_add("pydantic")

    def setup_gitignore(self):
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        self._copy_template(
            "Python.gitignore", package_filename=".gitignore", generic=True
        )

    def setup_vscode(self):
        path_to_vscode = self.path / ".vscode"
        os.makedirs(path_to_vscode, exist_ok=True)
        self._copy_template(
            "VSCode.settings.json", path_to_vscode, "settings.json", generic=True
        )
        self._copy_template(
            "VSCode.launch.json", path_to_vscode, "launch.json", generic=True
        )

    def setup_readme(self):
        """
        Set up README.md

        Use package name as title.
        Include template if exists
        Add a made with poetic line.
        """
        title = f"# {self.name}"
        readme_lines = [title + "\n\n"]
        readme_template_path = self._path_to_type_templates / "README.md"
        if readme_template_path.exists():
            with open(readme_template_path) as f:
                readme_lines += f.readlines()

        poetic_lines = []
        poetic_lines.append("\n-----\n")
        poetic_lines.append(f"*Made with {self._poetic_link}*\n")

        readme_lines += poetic_lines

        path_to_readme = self.path / "README.md"
        with open(path_to_readme, "w") as f:
            f.writelines(readme_lines)

    def post_init_commit(self):
        """
        Actions to be done after the initial commit.
        """
        pass

    def display(self):
        """
        Display the template via tree.
        """
        logg.info(self.name)
        for line in tree(self.path):
            logg.info(line)

    @abstractmethod
    def poetry_init(self):
        """
        Initialize package with poetry
        """
        if os.path.exists(self.name):
            raise PoeticException(
                f"{self.name} exists! Change name of new or existing package; or run with --update flag if you wish to update existing package."
            )

    @abstractmethod
    def setup_source_files(self):
        """
        Set up source files.
        """
        pass
