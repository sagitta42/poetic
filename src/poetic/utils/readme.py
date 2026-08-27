from pathlib import Path

from send2trash import send2trash

from poetic.utils.misc import POETIC_LINK
from poetic.utils.path import File


class Readme:
    """
    README manager.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._path_to_readme = self.path / "README.md"

    def add_section(self, title: str, header: int):
        """
        Add section to README.md.

        Construct section title based on header.
        Add empty line(s) above and below where needed.
        Appends section to existing readme.
        FIXME: is not smart to check whether section exists.
        """
        title_line = f"{'#'*header} {title}"

        title_lines = []
        if header > 1:
            title_lines.append("\n")
        title_lines.append(title_line)
        title_lines.append("\n")

        self.add_lines(title_lines)

    def add_lines(self, lines: list[str] | str):
        """
        Update README.md with given lines.

        Appends lines.
        """
        readme_lines = self.read()
        final_lines = readme_lines.copy()

        if len(final_lines) > 0:
            final_lines += ["\n"]

        lines_to_add = lines if isinstance(lines, list) else [lines]
        final_lines += lines_to_add

        self.write(final_lines)

    def update_from_template(self, path_to_template: Path):
        """
        Update README.md by appending lines from given path
        """
        with open(path_to_template) as f:
            template_lines = f.readlines()

        self.add_lines(template_lines)

    def add_poetic_line(self):
        """
        Add a made with poetic line to README if does not exist.
        """
        poetic_line = f"*Made with {POETIC_LINK}*\n"

        if not File(self._path_to_readme).has_line(poetic_line):
            lines = []
            lines.append("\n-----\n")
            lines.append(poetic_line)

            self.add_lines(lines)

    def read(self) -> list[str]:
        """
        Get README lines
        """
        ret = []
        if self._path_to_readme.exists():
            with open(self._path_to_readme) as f:
                ret = f.readlines()
        return ret

    def write(self, lines: list[str]):
        """
        Write README lines.
        """
        with open(self._path_to_readme, "w") as f:
            f.writelines(lines)

    def clean(self):
        """
        Delete README.md if exists.
        """
        if self._path_to_readme.exists():
            send2trash(self._path_to_readme)
