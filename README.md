# Poetic

A higher level wrapper for `poetry` that creates templates pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

### Command line

```bash
$ poetic -h
usage: poetic [-h] {template,add} ...

positional arguments:
  {template,add}
    template      create/update template
    add  
```

#### Create/update template

```bash
$ poetic template -h
usage: poetic template [-h] [--type {package,api}] [--db [{sqlite}]] [--settings] [--update] name

positional arguments:
  name                  Package name

options:
  -h, --help            show this help message and exit
  --type {package,api}  Template type
  --db [{sqlite}]  Create/update DB functionalities of given DB type
  --settings            Set up .env settings module
  --update              Update existing package

```

Example:
```bash
$ poetic awesome-package --type pacakge --settings
```

Available package types:
- `package` to create a package template (default)
- `api` to create an API template

Add `--db` flag to set up `alembic` migrations and DB of given type (applies to `api` template type only)

Available DB types:
- `sqlite` to set up a local SQLite DB (default)

Add `--settings` flag to set up `pydantic_settings` based `Settings` class containing `.env` variables (applies to `package` template only; API template always includes this class / source file)

Add `--update` flag to update existing poetic-made package repository after a poetic functionalities update.

#### Add functionality

```bash
$ poetic add -h
usage: poetic add [-h] {vscode,gitignore}

positional arguments:
  {vscode,gitignore}  Type of functionality

options:
  -h, --help          show this help message and exit
```

Single functionalities added to current directory:
- `poetic add vscode` - creates/updates `.vscode` setup
- `poetic add gitignore` - creates/updates `.gitignore`

If directory is a git repository, will commit if new setup or suggest commit if modified.

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

### `poetic template awesome-package --package --settings`

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
|       ├── py.typed # empty file that enables import suggestions in IDE
│       └── settings.py # pydantic_settings based Settings class containing .env variables
├── tests
|   ├── __init__.py
│   ├── conftest.py # set up to be able to run tests in dev mode
│   └──  test_unit.py # unit tests of awesome_package.foo and awesome_package.models.MyBaseModel
├── .gitignore # standard comprehensive Python .gitignore
├── .env.template
├── poetry.lock
├── pyproject.toml
├── README.md
└── venv # venv with pyproject.toml dependencies: dotenv; poetry and pytest (dev)
```

### `poetic template awesome-api --api --db`

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
├── app_info.py # app info extraction from pyproject
├── docker-compose.yml # API service
├── main.py # main API launcher
├── poetry.lock
├── pyproject.toml
├── README.md
├── settings.py # pydantic_settings based Settings class containing .env variables
└── venv # venv with pyproject.toml dependencies: dotenv; poetry and pytest (dev); fastapi, pydantic, pydantic-settings, uvicorn
```

### Update template

Add `--update` flag to `poetic template` call.

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

### Add functionality

```bash
$ poetic add vscode
VSCode update with [poetic](https://github.com/sagitta42/poetic)
├── settings.json
└── launch.json
```

## dev

### add new independent functionality item setup (`add`)

1. Create new `SetupType` e.g. `SetupType.foo`
1. Add `SetupType.foo` to `choices` for `type` argument of the microfunctionality subparser (`__main__.py`)
1. Create item settings `FooSettings` in `poetic.settings.item` inheriting from `SetupSettings` with `type` as `Literal[SetupType.foo]`
1. Add `FooSettings` to accepted setup settings in `poetic.settings.options`
1. Create item setup class `FooSetup` under `poetic.item` inheriting from `BaseFunctionalitySetup` or `BaseDependencySetup` if item includes python library dependency setup
1. Define `setup()` method, calling parent `setup()`, and adding specific setup actions for this item. This method must return `bool` representing whether this setup already existed before
1. In case of dependency setup, add dependencies in `setup_dependencies()` using `_poetry_add("package-name")`
1. Add `FooSetup` under `ItemSetupClass` enum in item builder, matching enum name with `SetupType` name (`foo`)

After this, this setup is now usable with `poetic add foo`

### `pydantic` <-> `argparse` adapter

Template and setup settings fields are used to set argparse descriptions, defaults, and options to avoid duplications.

For this reason, even if otherwise unnecessary:
- `default` for `type` is always set
- field type annotation is always set
- field description is always set