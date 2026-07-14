from abc import ABC, abstractmethod
from importlib import resources
import os
from pathlib import Path
import shutil
import subprocess
import venv

from poetic.git import Git
from poetic.logger import logg
from poetic.tree import tree


class GeneralTemplate(ABC):
    _TYPE: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._inner_name = self.name.replace("-", "_")
        self.path = Path(self.name)

        self._path_to_resources = Path(resources.files(__package__).__str__())
        self._path_to_templates = self._path_to_resources / "templates"
        self._path_to_type_templates = self._path_to_templates / self._TYPE

        self._git_auto = Git(self._path_to_resources.parent.parent)
        self._git_template = Git(self.path)

        logg.info(f"Setting up {self._TYPE}: {self.name}")

    def init(self):
        """
        Initial setup of the template.

        Initialize package with poetry.
        Set up files.
        Make initial commit.
        """
        self.poetry_init()
        self.setup()

        self._git_template.run("init")
        self._git_template.commit_all("template made with poetic")

        self.display()

    def update(self):
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
        current_branch = self._git_template.get_active_branch()
        update_branch = "dev-poetic-update"

        if not self._git_template.branch_exists(update_branch):
            first_commit = self._git_template.get_first_commit()
            self._git_template.run("branch", update_branch, first_commit)

        self._git_template.run("switch", update_branch)

        self.setup()

        last_poetic_commit = self._git_auto.get_last_commit()
        last_poetic_commit_message = self._git_auto.get_commit_message(
            last_poetic_commit
        )
        self._git_template.commit_all(
            f"poetic update\ncommit: {last_poetic_commit}\nmessage: {last_poetic_commit_message}"
        )

        self._git_template.run("switch", current_branch)
        self._git_template.run("merge", update_branch)

    def setup(self):
        """
        Template setup.

        Set up common files.
        Set up extra/specific files.
        """
        self.setup_gitignore()
        self.setup_dotenv_template()
        self.setup_dependencies()
        self.setup_source_files()
        self.setup_vscode()
        self.setup_readme()

        self.setup_extra()

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
        os.mkdir(path_to_vscode)
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
        readme_lines = [title + "\n"]
        readme_template_path = self._path_to_type_templates / "README.md"
        if readme_template_path.exists():
            with open(readme_template_path) as f:
                readme_lines += f.readlines()

        poetic_lines = []
        poetic_lines.append("\n-----\n")
        poetic_link = "[poetic](https://github.com/sagitta42/poetic)"
        poetic_lines.append(f"*Made with {poetic_link}*\n")

        readme_lines += poetic_lines

        path_to_readme = self.path / "README.md"
        with open(path_to_readme, "w") as f:
            f.writelines(readme_lines)

    def setup_extra(self):
        """
        Additional setup.
        """
        pass

    def display(self):
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
        generic: bool = False,
    ):
        """
        Copy template into package source code.

        template_filename (str): name of template to copy contained under templates of this package
        generic (bool): template is generic (independent of setup type)
        path_in_package (Path | None): path where to copy in package; default = root path
        package_filename (str | None): filename of template in package; default = same as original template
        """
        path_in_package = path_in_package or self.path
        package_filename = package_filename or template_filename

        path_to_templates = (
            self._path_to_templates if generic else self._path_to_type_templates
        )

        shutil.copy(
            path_to_templates / template_filename,
            path_in_package / package_filename,
        )

    def _poetry_add(self, package: str, group: str | None = None):
        args = ["poetry", "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)
        args.append("--lock")

        subprocess.run(
            args,
            cwd=self.path,
            env={
                **os.environ,
                "PATH": str(self.venv / "bin") + ":" + os.environ["PATH"],
                "POETRY_VIRTUALENVS_CREATE": "false",
            },
        )

    def _run(self, commands: list[str]):
        """
        Simple command run in template root directory.
        """
        subprocess.run(commands, cwd=self.path)

    @property
    def venv(self) -> Path:
        path_to_venv = self.path / "venv"
        if not path_to_venv.exists():
            venv.create(path_to_venv, with_pip=True)
            subprocess.run([path_to_venv / "bin" / "pip", "install", "poetry"])
        return path_to_venv
