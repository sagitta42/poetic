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