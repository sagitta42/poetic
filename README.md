# Poetic

A higher level wrapper for `poetry` that creates templates pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

### Command line

```python
$ python -m poetic <package-name> --type <package-type> [--db] [<db-type>] [--update] 
```

Available package types:
- `package` to create a package template (default)
- `api` to create an API template

Add `--db` flag to set up `alembic` migrations and DB of given type (applies to `api` template type only)

Available DB types:
- `sqlite` to set up a local SQLite DB (default)

Add `--update` flag to update existing poetic-made package repository after a poetic functionalities update.

### In code

For package template:

```python
from poetic import PackageTemplate

package_template = PackageTemplate("awesome-package")
package_template.init()
```

Use `APITemplate` instead for API template.

Use `packge_template.update()` instead to update existing package.

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

### `python -m poetic awesome-api --api --db`

Result

```bash
awesome-api
├── .vscode
│   ├── launch.json # debug test setup
│   └── settings.json # pytest, format on save, pylance, auto-import, ...
├── alembic_migrations
│   ├── alembdantic # pydantic controlled alembic
│   │   ├── opd.py # pydantic controlled alembic.op
│   │   └── table_model.py # base class for alembdantic tables
│   ├── versions
|   |   └── 2026_07_15_143709-36648a63d305-example.py # example migration using alembdantic
│   ├── env.py # alembic env with DB URL based on .env
│   ├── models.py # example alembdantic table schema
│   ├── README
│   └── script.py.mako
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
├── db
│   └── db.db # initial committed SQLite DB file
├── .gitignore  # standard comprehensive Python .gitignore
├── .env.template
├── alembic.ini
├── config.py # app info and settings
├── docker-compose.yml # API service
├── main.py # main API launcher
├── poetry.lock
├── pyproject.toml
├── README.md
└── venv # venv with pyproject.toml dependencies: dotenv; poetry and pytest (dev); fastapi, pydantic, pydantic-settings, uvicorn
```

### Update

On the first update, will create a branch dedicated to poetic updates starting from the first commit.

```bash
$ git branch
  dev-poetic-update
* main
```

The standard setup is run in the update branch, and the differences/additions are committed and merged with the active branch.

```bash
commit cac874d5f2cf07199f00890c4d4cefbb57d3206b (HEAD -> main)
Merge: a01eefc b4bb541
    Merge branch 'dev-poetic-update'

commit b4bb54109bf78b85618566c3df082128a3f93dd8 (dev-poetic-update)
    poetic update
    commit: d68f600af54ae2410557d19a5f72b09ed63aadbe
    message: <last poetic commit message>

commit a01eefcfe8fff4372c9ad337d40e9ad991b32f9d
    readme update

commit d68f600af54ae2410557d19a5f72b09ed63aadbe
    template made with poetic
```
