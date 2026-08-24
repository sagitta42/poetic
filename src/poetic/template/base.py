from abc import abstractmethod
import os
from pathlib import Path
from typing import TypeVar

from poetic.exceptions import PoeticException
from poetic.item.gitignore import GitignoreSetup
from poetic.item.env_settings import EnvSettingsSetup
from poetic.item.vscode import VSCodeSetup
from poetic.settings.template import BaseTemplateSettings
from poetic.logger import logg

from poetic.setup.dependency import BaseDependencySetup
from poetic.utils.toml import PyProjectHandler
from poetic.utils.tree import display

T_TemplateSettings = TypeVar("T_TemplateSettings", bound=BaseTemplateSettings)


class BaseTemplate(BaseDependencySetup[T_TemplateSettings]):
    """
    General template setup.

    Included functionalities setup:
        - gitignore
        - VSCode

    Repository setup:
        - source files
        - README

    Operations
        - repository init (git, poetry)
        - repository setup
        - repository update

    Repository update: updating existing template with poetic updates.
    """

    def __init__(self, settings: T_TemplateSettings, root_path: Path | None) -> None:
        """
        Initialize template setup with given settings.

        root_path (Path): path in which to do the setup. Used mainly for testing/debug.
            Default None -> setup path is same as package name. Otherwise prepend path
        """
        self.name = settings.name

        template_path = Path(self.name)
        if root_path is not None:
            template_path = root_path / template_path

        super().__init__(template_path, settings, core=True)

        self._inner_name = self.name.replace("-", "_")

        # self._git_auto = Git(self._path_to_resources.parent.parent)

        self._env_settings_setup: EnvSettingsSetup | None = None
        self._vscode = VSCodeSetup(self.path)
        self._gitignore = GitignoreSetup(self.path)
        self._pyproject_handler = PyProjectHandler(self.path)

        logg.info(f"Setting up {self._type}: {self.name}")

    def launch(self) -> None:
        """
        Template launch action.

        Update/create based on request.
        """
        if self._settings.update:
            self.update()
        else:
            self.init()

    def init(self):
        """
        Initial setup of the template.

        Initialize package with poetry. Register resulting initial pyproject.toml.
        Initialize git repository.
        Set up repository.
        Make initial commit.
        Perform post-commit setup.
        """
        self.poetry_init()

        self.git.run("init")

        self.setup()

        self.git.commit_all(f"template made with {self._poetic_link}")

        logg.info(f"Template setup DONE", header=True)
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

    def setup(self) -> None:
        """
        Main setup.

        Additional setup: set up repository.

        Set up standard Python gitignore.
        Set up source files.
        Set up pydantic-settings class for if requested.
        Set up .vscode launch and settings.
        Set up README file.
        Set up pyproject.toml.
        """
        super().setup()

        self._gitignore.setup()
        self.setup_source_files()

        if self._env_settings_setup is not None:
            self._env_settings_setup.setup()
        self._vscode.setup()

        self.setup_readme()
        self.setup_pyproject()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("pydantic")

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

    def setup_pyproject(self):
        """
        Set up pyproject.toml.

        Set up poetic section in pyproject.toml.
        """
        self._pyproject_handler.read()
        self._pyproject_handler.add_section(
            "tool.poetic", self._settings.core_settings()
        )
        self._pyproject_handler.save_toml()

    def display(self, suggest_commit: str | None = None):
        """
        Display the template via tree.
        """
        logg.info(self.name)
        display(self.path)

    @abstractmethod
    def poetry_init(self):
        """
        Initialize package with poetry.
        """

        if os.path.exists(self.path):
            raise PoeticException(
                f"{self.name} exists! Change name of new or existing package; or run with --update flag if you wish to update existing package."
            )

    @abstractmethod
    def setup_source_files(self):
        """
        Set up source files.
        """
        pass
