# Poetic

A higher level wrapper for `poetry` that creates a package template pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

```python
from poetic import setup_package_template
setup_package_template("awesome-package")
```

Result

```bash
├── .git # initial commit of this template
├── .vscode
│   └── settings.json # pytest Testing Suite setup
├── README.md
├── poetry.lock
├── venv # contains poetry, dotenv, and pytest (dev)
├── src
│   └── awesome_package
│       ├── __init__.py
│       ├── foo.py
│       ├── logger.py # log with levels based on .env
│       └── core.py
├── pyproject.toml
├── .gitignore # standard comprehensive Python .gitignore
└── tests
    ├── __init__.py
    ├── test_foo.py # test of src/awesome_package/foo.py
    └── conftest.py # set up to be able to run tests in dev mode
```

