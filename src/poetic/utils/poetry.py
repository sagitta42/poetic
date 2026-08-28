from poetic.command_runner import BaseCommandRunner


class Poetry(BaseCommandRunner):
    def init_basic(self, name: str | None = None):
        """
        Basic poetry init with no structure.
        """
        package_name = name or self.path.stem
        self.run(
            "poetry",
            "init",
            "--no-interaction",
            "--name",
            package_name,
            "--description",
            "",
        )
