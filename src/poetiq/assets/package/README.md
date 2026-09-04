
## Usage

```bash
>>> from $PACKAGE import is_answer
>>> is_answer(42)
True
>>> is_answer(43)
False
```

## For dummies / development notes

Local install

```bash
pip install /path/to/$package
```

Run tests
```bash
cd /path/to/$package
source venv/bin/activate
```

Option 1: run `poetry install` to install this package into its own `venv`

Option 2: set up debug environment `cp .env.template` to make source files visible to `pytest`.

Then, run `pytest`.

Note: `poetiq` has already fully set up `venv` for you, including installing `pytest`.

Add remote
```bash
git remote add origin https://...
```