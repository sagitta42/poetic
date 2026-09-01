# Poetic

A higher level wrapper for `poetry` that creates templates pre-filled with basic structure and setup that I find convenient as a starting point for my packages.

- [Usage](#usage): command line usage with examples
- [Examples](#examples): examples of templates and functionalities results
- [development notes](#development-notes): notes on how to add new features to `poetic`

## Install

```bash
pip install git+https://github.com/sagitta42/poetic.git
```

## Usage

```bash
$ poetic -h
usage: poetic [-h] {new,init,add,update,setup,install} ...

positional arguments:
  {new,init,add,update,setup,install}
    new                 create new template
    init                basic no-interaction init
    add                 poetry add with git+ auto-detect
    update              update current template as is with new poetic updates
    setup               setup functionality in existing repo/directory
    install             poetry install with added options

options:
  -h, --help            show this help message and exit
```

### Create template

```bash
$ poetic new -h
usage: poetic new [-h] [--type [{package,app}]] [--db-type [{sqlite,psql,none}]] [--dev-sqlite] [--pydantic-table] [--mongodb] [--settings] [--progressbar] name

positional arguments:
  name                  Template/repository name

options:
  -h, --help            show this help message and exit
  --type [{package,app}]
                        Type of functionality
  --db-type [{sqlite,psql,none}]
                        Database type (app only)
  --dev-sqlite          Development mode switch to SQLite (app only)
  --pydantic-table      Set up pydantic-table for alembic migrations (app only)
  --mongodb             Add MongoDB service (app only)
  --settings            Set up .env Settings class (package only)
  --progressbar         Set up progress bar source code (package only)
```

Main note: `poetry new package-name` complains if directory `package-name` already exists; `poetic new package-name` only complains if it is non-empty

Example:
```bash
$ poetic new awesome-package --type pacakge --settings
```

Available package types:
- `package` to create a package template (default)
- `app` to create a simple web app template

Add `--db` flag to set up `alembic` migrations and DB of given type (applies to `app` template type only)

Available DB types:
- `sqlite` to set up a local SQLite DB (default)
- `psql` to set up PostgreSQL service in `docker-compose.yml`

Add `--dev-sqlite` flag to set up dual psql/SQLite setup with switch to SQLite via `.env` variables for local development testing.

Add `--mongodb` flag to set up MongoDB service in `docker-compose.yml` and related source files and dependencies in the app code (app only).

Add `--settings` flag to set up `pydantic_settings` based `Settings` class containing `.env` variables (applies to `package` template only; app template always includes this class / source file)

Add `--progressbar` flag to set up a simple `ProgressBar` util class in a package source file.

See detailed examples in [Template examples](#templates)

### Init template

`poetic init -h` to init a simple template in current direcotry with most basic no-interaction poetry pyproject init. Will treat current directory name as project name.

### Add dependency

```bash
$ poetic add -h
usage: poetic add [-h] [--local [LOCAL]] package

positional arguments:
  package          Package source (name, https, git)

options:
  -h, --help       show this help message and exit
  --local [LOCAL]  Add local dependency to poetic.toml
```

Running `poetic add package-name` is equivalent to `poetry add package-name`.

Adding package from a repository, running `poetic add https://github.com/username/awesome-package` will automatically add `git+` (same for `ssh` hosted `git@...`)

Use `--local` flag and path to a local clone/repository as `poetic add package-name --local /path/to/awesome-package` to add local dependency to `poetic.toml` - see [Install](#install) for `poetic install --local` usage to handle dual dependencies.

### Update template

Run `poetic update` inside an existing poetic template to update it after poetic itself was updated (new functionalities, bugfixes).

The update will create a special separate update branch, run poetic template setup in it, and then merge the branch into the one you started from. This way, the updates do not all overwrite the changes you made afterwards. Make sure to handle the merge manually anyway, and be able to recover your original setup in case the merge it too complex.

See detailed examples in [Template examples](#templates)

### Set up functionality

```bash
$ poetic setup -h
usage: poetic setup [-h] [--db-type [{sqlite,psql}]] [--dev-sqlite] [--pydantic-table] [--subfolder [SUBFOLDER]] [--no-commit] {vscode,gitignore,db,logger}

positional arguments:
  {vscode,gitignore,db,logger}
                        Type of functionality

options:
  -h, --help            show this help message and exit
  --db-type [{sqlite,psql}]
                        Database type (db only)
  --dev-sqlite          Development mode switch to SQLite (db only)
  --pydantic-table      Set up pydantic-table for alembic migrations (db only)
  --subfolder [SUBFOLDER]
                        Subfolder of setup (logger only)
  --no-commit           Do not commit changes
```

Single functionalities set up in current directory:
- `poetic setup vscode` - creates/updates `.vscode` setup
- `poetic setup gitignore` - creates/updates `.gitignore`
- `poetic setup db --db psql --dev-sqlite` - sets up psql DB with dev mode switch to SQLite

If directory is a git repository, will commit changes unless `--no-commit` flag is provided.

See detailed examples in [Functionality setup examples](#functionalities)

### Install

```bash
$ poetic install -h
usage: poetic install [-h] [--local]

options:
  -h, --help  show this help message and exit
  --local     Install local dependencies defined in .poetic.toml
```

Perform smart poetry install: automatically add `--no-root` flag if current directory `pyproject.toml` states `package-mode=false`

Add `--local` flag if you want to install the dependences in `pyproject.toml` from filepath instead of pyproject information (e.g. a local clone of a dependency, which may be convenient during development)

Provide paths to local dependencies via `.poetic.toml` file. Format:
```toml
[dependency-groups]
local = [
  "my-package @ /path/to/my-package",
  "python-module @ /path/to/my/fork/of/python-module",
]
```
or by running `poetic add my-package --local /path/to/my-package` (see [Add dependency](#add-dependency) section)

Specify a packge to perform local install with `poetic install --local my-package` or simply `--local` to perform local install for all dual packages.

See detailed examples in [Install examples](#install-examples)

## Examples

### Templates

#### `poetic new awesome-package --type package --settings --progressbar`

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
|       ├── progressbar.py # ProgressBar wrapper class if requested
│       └── settings.py # pydantic_settings based Settings class containing .env variables if requested
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

#### `poetic new awesome-app --type app --db psql --dev-sqlite --mongodb`

Result

```bash
awesome-app
├── .vscode
│   ├── launch.json # debug test setup
│   └── settings.json # pytest, format on save, pylance, auto-import, ...
├── alembic_migrations # migrations for SQLite if requested; adaptation for PostgreSQL coming soon
│   ├── versions
│   ├── env.py # auto DB URL using settings.py - compatible with SQLite/psql via only .env change
│   ├── README
│   └── script.py.mako
├── app
│   ├── api
│   │   ├── routes
│   │   │   └── dummy.py
│   │   └── router.py # main API router that includes dummy router
│   ├── schemas
│   │   └── dummy.py # dummy request and response schemas
│   └── services
│       └── dummy.py # dummy service using dummy core logic
├── core
│   ├── models
│   │   ├── example.py # DeclarativeBase for sqlalchemy session
│   │   └── mongo_document.py
│   ├── db.py # DB session with automatic dual SQLite/psql switch based on .env
│   ├── db_mongo.py # dummy MongoDB client
│   ├── dummy.py # dummy core logic
│   └── mongo_config.py # MongoDB client config using settings.py
├── db
│   └── database.db # initial SQLite DB file, not tracked
├── venv # venv with pyproject.toml dependencies installed: dotenv, fastapi, pydantic, ...
├── .env.template # controls switch from SQLite to psql with just a few variables
├── .gitignore # standard comprehensive Python .gitignore
├── alembic.ini
├── app_info.py # app info extraction from pyproject
├── docker-compose.yml # app, psql, and mongodb services, env variables set based on .env
├── dockerfile # app service dockerfile
├── main.py # main API launcher
├── poetic.toml.template
├── poetry.lock
├── pyproject.toml
├── README.md
└── settings.py  # pydantic_settings based Settings class containing .env variables for sqlite/psql dual setup and MongoDB; shared by alembic migrations, SQLAlchemy Session, and MongoDB client
```

#### Update template

`poetic update`

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

### Functionalities

```bash
$ poetic setup vscode
VSCode update with [poetic](https://github.com/sagitta42/poetic)
├── settings.json
└── launch.json
```

### Install examlpes

Poetic automatically determines `--no-root` flag analyzing `pyproject.toml` for `package-mode=false`:

```bash
$ poetic install --local
Local install requested but no dual dependencies found in .poetic.toml
poetic: poetry install --no-root
Installing dependencies from lock file

No dependencies to install or update
```

Poetic uninstalls and re-installs dual dependencies:
```bash
$ poetic install --local
poetic: poetry install --no-root
Installing dependencies from lock file

No dependencies to install or update
Replacing dual packages with local dependencies
poetic: pip uninstall python-module
Found existing installation: python-module 2.13.4
Uninstalling python-module-2.13.4:
  Would remove:
    /home/user/path/to/repo/venv/lib/python3.12/site-packages/python-module-2.13.4.dist-info/*
    /home/user/path/to/repo/venv/lib/python3.12/site-packages/python-module/*
Proceed (Y/n)? 

...

poetic: pip install /path/to/my/fork/of/python-module
Processing /path/to/my/fork/of/python-module

...

Successfully installed python-module-2.14.0a1 ...
```

with `.poetic.toml`:
```toml
[poetic]
local_dependencies = [
  "python-module @ /path/to/my/fork/of/python-module",
]
```

## development notes

### implement new independent functionality item setup (`setup`)

1. Create new `SetupType` e.g. `SetupType.foo` (`settings.setup`)
1. Add `SetupType.foo` to `choices` for `type` argument of the microfunctionality subparser in `add_microfunctionality_arguments()` (`cli/cli.py`)
1. Create item settings `FooSettings` in `poetic.settings.item` inheriting from `SetupSettings` with `type` as `Literal[SetupType.foo]`
1. Add additional settings field if any under `FooSettings` e.g. `field`
1. Create function adding those settings to given CLI parser in `cli/cli.py` e.g. `add_foo_arguments(parser)` utilizing `FooSettings` to translate them to CLI arguments. Append call to this function under `add_microfunctionality_arguments()`
1. Add `FooSettings` to accepted setup settings ( `settings.options`)
1. Create item setup class `FooSetup` in a new source file `poetic.item.foo` inheriting from a base setup (e.g. `BaseFunctionalitySetup`, `BaseVenvSetup`, or `BaseDependencySetup` )  with `[FooSettings]` (`Generic`) depending on if item includes python library dependency setup etc. For convenience, define `__init__()` with `settings=FooSettings()`
1. Define `setup()` method, calling parent `setup()`, and adding specific setup actions for this item. This method must return `bool` representing whether this setup already existed before.
1. In case of dependency setup, add dependencies in `setup_dependencies()` using `_poetry_add("package-name")`
1. Add `FooSetup` under `ItemSetupClass` enum in `item.builder`, matching enum name with `SetupType` name (`foo`)

After this, this setup is now usable with `poetic add foo`

### implement new DB setup

1. Define new DB type in `DBType` e.g. `DBType.foo`
1. Create DB setup class `FooDBSetup` inheriting from `BaseDBSetup`
1. Define its `setup_db()` method with actions for this DB setup. Return bool representing whether this setup existed before
1. Define DB URL under `db_url` property
1. Add `FooDBSetup` under `DBSetupClass` in `poetic.item.db.builder` using the same enum name as defined `DBType` (`foo`)

After this, this setup is now usable with
- `poetic new awesome-app --db psql`
- `poetic setup db --db foo`

### `pydantic` <-> `argparse` adapter

Template and setup settings fields are used to set argparse descriptions, defaults, and options to avoid duplications.

For this reason, even if otherwise unnecessary:
- `default` for `type` is always set
- field type annotation is always set
- field description is always set

### build assets

To run tests locally, need to first run `poetry build` to generate `src/poetic/_build_assets` (see `build.py`) for non-src assets