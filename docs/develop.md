
# Develop requirements 

Tested on the following versions:

 - python : `3.9.4`
 - docker : `24.0.5`
 - torch : `2.0.1`

# Getting Started

Install venv
```bash
python -m venv .venv
. .venv/bin/activate
python -V
```
# How to setup

```sh
pip install -r requirements.txt
```
> For Development
```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Set `PYTHONPATH`
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo $PYTHONPATH
```

# Method of Contributing to Open Source

Before commit,

Use `isort` to reorder package import and reformat using autu linter `black`.
Use `pylint` for static code analysis
```sh
isort <Project-Root-Path>
black <Project-Root-Path>
pylint <Project-Root-Path>
pytest <Project-Root-Path>
```

