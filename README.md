# Poetic

A higher level wrapper for `poetry` that creates templates pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

### Command line

```python
$ python -m poetic <package-name> --<flag>
```

Available flags:
- `--package` to create a package template
- `--api` to create an API template

### In code

For package template:

```python
from poetic import PackageTemplate

package_template = PackageTemplate("awesome-package")
package_template.setup()
```

Use `APITemplate` instead for API template.

## Examples

### `python -m poetic awesome-package --package`

Result

```bash
awesome-package
├── .vscode
│   ├── launch.json # debug test setup
│   └── settings.json # pytest, format on save, pylance, auto-import, ...
├── src
│   └── awesome_package
│       ├── __init__.py # imports * from core.py
│       ├── foo.py # example source file
│       ├── logger.py # log with levels based on .env and color/bold functionalities
│       ├── core.py # everything here is imported in __init__ as core functionality
|       └── py.typed # empty file that enables import suggestions in IDE
├── tests
|   ├── __init__.py
│   ├── conftest.py # set up to be able to run tests in dev mode
│   └──  test_foo.py # test of src/awesome_package/foo.py
├── .gitignore # standard comprehensive Python .gitignore
├── .env.template
├── poetry.lock
├── pyproject.toml
├── README.md
└── venv # venv with pyproject.toml dependencies: dotenv; poetry and pytest (dev)
```

### `python -m poetic awesome-api --api`

Result

```bash
awesome-api
├── .vscode
│   ├── launch.json # debug test setup
│   └── settings.json # pytest, format on save, pylance, auto-import, ...
├── app
│   ├── services
│   │   └── dummy.py # dummy service using dummy core logic
│   ├── schemas
│   │   └── dummy.py # dummy request and response schemas
│   └── api
│       ├── router.py # main API router that includes dummy router
│       └── routes
│           └── dummy.py # dummy router with a single endpoint calling dummy service
├── core
│   └── dummy.py # dummy core logic
├── .gitignore  # standard comprehensive Python .gitignore
├── .env.template
├── config.py # app info and settings
├── main.py # main API launcher
├── poetry.lock
├── pyproject.toml
├── README.md
└── venv # venv with pyproject.toml dependencies: dotenv; poetry and pytest (dev); fastapi, pydantic, pydantic-settings, uvicorn
```