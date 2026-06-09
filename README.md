# Poetic

A higher level wrapper for `poetry` that creates a package template pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

```python
$ python -m poetic awesome-package
```

Result

```bash
awesome-package
├── README.md
├── venv # contains poetry, dotenv, and pytest (dev)
├── src
│   └── awesome_package
│       ├── __init__.py
│       ├── foo.py # example source file
│       ├── logger.py # log with levels based on .env
│       └── core.py # everything here is imported in __init__ as core functionality
├── .vscode
│   ├── launch.json # debug test setup
│   └── settings.json # pytest, format on save, pylance, auto-import, ...
├── .gitignore # standard comprehensive Python .gitignore
├── .env.template
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── test_foo.py # test of src/awesome_package/foo.py
│   ├── __init__.py
│   └── conftest.py # set up to be able to run tests in dev mode
└── .git # initial commit of this template
```

Suggestion: install into main venv and create alias function in `.bash_aliases` or `.bashrc`: 

```bash
function poetic(){
    python -m poetic $1
}
```
to run
```bash
$ poetic awesome-package
```
directly