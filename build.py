import shutil
from pathlib import Path

# def build(setup_kwargs=None):
#     src = Path(".vscode")
#     dst = Path("src/poetic/_build_assets")
#     if dst.exists():
#         shutil.rmtree(dst)
#     shutil.copytree(src, dst)


def build(setup_kwargs=None):
    internal_assets = [".vscode", ".gitignore"]
    dst = Path("src/poetic/_build_assets")

    if dst.exists():
        shutil.rmtree(dst)

    for ass in internal_assets:
        ass_path = Path(ass)
        copy_function = shutil.copytree if ass_path.is_dir() else shutil.copy
        copy_function(ass_path, dst)


if __name__ == "__main__":
    build()
