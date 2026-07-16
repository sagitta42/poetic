from abc import abstractmethod
from importlib import resources
import os
from pathlib import Path
import shutil
import subprocess
from typing import Generic, TypeVar
import venv

from poetic.git import Git
from poetic.logger import logg
from poetic.settings import TemplateSettings
from poetic.tree import tree

T_Settings = TypeVar("T_Settings", bound=TemplateSettings)


class BaseTemplate(Generic[T_Settings]):
    def __init__(self, settings: T_Settings) -> None:
        self.name = settings.name
        self._type: str = settings.type.value

        self._inner_name = self.name.replace("-", "_")
        self.path = Path(self.name)
        self._path_to_venv = (self.path / "venv").resolve()

        self._path_to_resources = Path(resources.files(__package__).__str__())
        self._path_to_templates = self._path_to_resources / "templates"
        self._path_to_type_templates = self._path_to_templates / self._type

        # self._git_auto = Git(self._path_to_resources.parent.parent)
        self.git = Git(self.path)

        self._poetic_link = "[poetic](https://github.com/sagitta42/poetic)"

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

    def setup(self):
        """
        Template setup.

        Set up common files.
        Set up extra/specific files.
        """
        self.setup_gitignore()
        self.setup_dotenv_template()
        self.setup_venv()
        self.setup_dependencies()
        self.setup_source_files()
        self.setup_vscode()
        self.setup_readme()

        self.setup_extra()

    def setup_venv(self):
        """
        Set up venv.

        Create venv.
        Install poetry into that venv.
        """
        if not self._path_to_venv.exists():
            venv.create(self._path_to_venv, with_pip=True)
        self._run(self.venv("pip"), "install", "poetry", env=True)

    def setup_dependencies(self):
        self._poetry_add("dotenv")

    def setup_gitignore(self):
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        self._copy_template(
            "Python.gitignore", package_filename=".gitignore", generic=True
        )

    def setup_dotenv_template(self):
        """
        Set up .env.template
        """
        self._copy_template(".env.template", generic=True)

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

    def setup_extra(self):
        """
        Additional setup.
        """
        pass

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
        pass

    @abstractmethod
    def setup_source_files(self):
        """
        Set up source files.
        """
        pass

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
        template_subdir: Path | str | None = None,
        generic: bool = False,
    ) -> Path:
        """
        Copy template into package source code.

        template_filename (str): name of template to copy contained under templates of this package
        generic (bool): template is generic (independent of setup type)
        path_in_package (Path | None): path where to copy in package; default = root path
        package_filename (str | None): filename of template in package; default = same as original template

        Returns path to file in package.
        """
        path_to_template = self._get_template_path(
            template_filename, generic, template_subdir=template_subdir
        )

        path_in_package = path_in_package or self.path
        package_filename = package_filename or template_filename
        path_to_package_file = path_in_package / package_filename

        shutil.copy(path_to_template, path_to_package_file)

        return path_to_package_file

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = [self.venv("poetry"), "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)

        self._run(*args, env=True)

    def _get_template_path(
        self, template_filename: str, generic: bool, template_subdir: Path | str | None
    ) -> Path:
        """
        Get path given template.
        """
        path_to_templates = (
            self._path_to_templates if generic else self._path_to_type_templates
        )
        if template_subdir is not None:
            path_to_templates = path_to_templates / template_subdir

        ret = path_to_templates / template_filename
        return ret

    def _run(self, *args, env: bool = False):
        """
        Run command in template root directory.
        """
        subprocess.run(
            args,
            cwd=self.path,
            env=(
                {
                    **os.environ,
                    "POETRY_VIRTUALENVS_CREATE": "false",
                    "VIRTUAL_ENV": self._path_to_venv,
                }
                if env
                else None
            ),
        )

    def venv(self, exe: str) -> Path:
        """
        Get venv path to executable.
        """
        ret = self._path_to_venv / "bin" / exe
        return ret
