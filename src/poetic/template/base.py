from abc import abstractmethod
from pathlib import Path
from typing import TypeVar

from poetic.exceptions import PoeticException
from poetic.item.env_settings import EnvSettingsSetup
from poetic.settings.template import BaseTemplateSettings
from poetic.logger import logg

from poetic.setup.poetry import BasePoetrySetup
from poetic.utils.path import Dir
from poetic.utils.tree import display
from poetic.utils.misc import POETIC_LINK

T_TemplateSettings = TypeVar("T_TemplateSettings", bound=BaseTemplateSettings)


class BaseTemplate(BasePoetrySetup[T_TemplateSettings]):
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

    def __init__(self, settings: T_TemplateSettings, path: Path | None) -> None:
        """
        Initialize template setup with given settings.

        path (Path): path in which to do the setup.
            Default (None): package name
        """
        self.name = settings.name

        template_path = path or Path(self.name)

        super().__init__(template_path, settings, core=True)

        self._inner_name = self.name.replace("-", "_")

        # self._git_auto = Git(self._path_to_resources.parent.parent)

        self._env_settings_setup: EnvSettingsSetup | None = None

        logg.info(f"Setting up {self._type.value}: {self.name}")

    def launch(self) -> None:
        """
        Template launch action: init template
        """
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

        self.global_setup()

        self.git.commit_all(f"template made with {POETIC_LINK}")

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

        self.global_setup()

        # FIXME: correctly get poetic commits
        # last_poetic_commit = self._git_auto.get_last_commit()
        # last_poetic_commit_message = self._git_auto.get_commit_message(
        # last_poetic_commit
        # )
        # message = f"{self._poetic_link} update\ncommit: {last_poetic_commit}\nmessage: {last_poetic_commit_message}"

        message = f"latest {POETIC_LINK} update"
        self.git.commit_all(message)

        self.git.run("switch", current_branch)
        self.git.run("merge", update_branch)

    def setup(self) -> None:
        """
        Main setup.

        Set up source files.
        Set up pydantic-settings class for if requested.
        Set up .vscode launch and settings.
        Set up pyproject.toml.
        Set up poetic.toml.template.
        """
        super().setup()

        self.setup_source_files()

        if self._env_settings_setup is not None:
            self._env_settings_setup.setup()
        self._vscode.setup()

        self.setup_pyproject()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("pydantic")

    def setup_readme(self):
        """
        Set up README.md

        Set up fresh readme.
        Use package name as title.
        Include template if exists.
        """
        super().setup_readme()
        logg.info("...creating README.md", header=True)

        self._readme.clean()
        self._readme.add_section(self.name, header=1)

        readme_template_path = self._templates.get_filepath("README.md")
        if readme_template_path.exists():
            self._readme.update_from_template(readme_template_path)

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

        Check if setup path directory already exists and contains files.
        """

        if Dir(self.path).exists_and_non_empty():
            raise PoeticException(
                f"{self.name} exists and non-empty! Change name or (re)move existing packge; or run poetic update inside existing package if you wish to update it."
            )

    @abstractmethod
    def setup_source_files(self):
        """
        Set up source files.
        """
        pass
